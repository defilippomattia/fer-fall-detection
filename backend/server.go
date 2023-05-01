package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"

	"github.com/redis/go-redis/v9"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type AlertMsg struct {
	Id         primitive.ObjectID `bson:"_id,omitempty"`
	SourceType string             `json:"source_type"`
	SourceID   string             `json:"source_id"`
	Longitude  string             `json:"longitude"`
	Latitude   string             `json:"latitude"`
	Timestamp  string             `json:"timestamp"`
	Comment    string             `json:"comment"`
	Resolved   bool               `json:"resolved"`
}

type HandlersDependencies struct {
	mongoClient *mongo.Client
	redisClient *redis.Client
}

// write function get db client
func getMongoClient() (*mongo.Client, error) {
	//later will come from config file
	// host := os.Getenv("FFD_MONGO_HOST")
	// port := os.Getenv("FFD_MONGO_PORT")
	// user := os.Getenv("FFD_MONGO_USER")
	// password := os.Getenv("FFD_MONGO_PASSWORD")

	host := "mongo-container"
	port := "27017"
	user := "root"
	password := "root"

	connectionURI := fmt.Sprintf("mongodb://%s:%s@%s:%s", user, password, host, port)

	// Create a new client
	client, err := mongo.NewClient(options.Client().ApplyURI(connectionURI))
	if err != nil {
		return nil, err
	}
	// Connect to the MongoDB server
	err = client.Connect(context.Background())
	if err != nil {
		return nil, err
	}
	// Verify the connection by pinging the server
	err = client.Ping(context.Background(), nil)
	if err != nil {
		return nil, err
	}

	return client, nil
}

func getRedisClient() (*redis.Client, error) {
	//later will come from config file
	// host := os.Getenv("FFD_REDIS_HOST")
	// port := os.Getenv("FFD_REDIS_PORT")
	dum := os.Getenv("TA")
	fmt.Println(dum)
	host := "redis-container"
	port := "6379"

	connectionURI := fmt.Sprintf("%s:%s", host, port)

	// Create a new client
	client := redis.NewClient(&redis.Options{
		Addr: connectionURI,
	})
	// Verify the connection by pinging the server
	_, err := client.Ping(context.Background()).Result()
	if err != nil {
		return nil, err
	}

	return client, nil
}

func getAlertsHandler(w http.ResponseWriter, r *http.Request, deps *HandlersDependencies) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PATCH")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	allAlerts := []AlertMsg{}
	client := deps.mongoClient
	collection := client.Database("fer-fall-detect").Collection("alerts")

	// Query the MongoDB database to retrieve all alerts
	cursor, err := collection.Find(context.Background(), bson.M{})
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	defer cursor.Close(context.Background())

	// Decode the alerts and store them in a slice of AlertMsg structs
	for cursor.Next(context.Background()) {
		var alert AlertMsg
		if err := cursor.Decode(&alert); err != nil {
			log.Println(err)
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		allAlerts = append(allAlerts, alert)
	}
	if err := cursor.Err(); err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Encode the slice of AlertMsg structs as JSON
	jsonBytes, err := json.Marshal(allAlerts)
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	// Write the JSON response back to the client
	w.WriteHeader(http.StatusOK)
	w.Write(jsonBytes)

}

func patchAlertsHandler(w http.ResponseWriter, r *http.Request, deps *HandlersDependencies) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS,PATCH")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	fmt.Println("patchAlertsHandler")
	var requestBody map[string]interface{}
	rb := r.Body
	err := json.NewDecoder(rb).Decode(&requestBody)

	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	Id, ok := requestBody["Id"].(string)
	if !ok {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	oid, err := primitive.ObjectIDFromHex(Id)
	if err != nil {
		http.Error(w, "Invalid ObjectID", http.StatusBadRequest)
		return
	}

	filter := bson.M{"_id": oid}

	fmt.Println("Id: ", Id)

	client := deps.mongoClient
	update := bson.M{}
	for key, value := range requestBody {
		if key != "Id" {
			update[key] = value
		}
	}

	_, err = client.Database("fer-fall-detect").Collection("alerts").UpdateOne(context.Background(), filter, bson.M{"$set": update})
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// retrieve the updated document from the collection
	var updatedAlert AlertMsg
	err = client.Database("fer-fall-detect").Collection("alerts").FindOne(context.Background(), filter).Decode(&updatedAlert)
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// encode the updated document as JSON and return it as the response
	response, err := json.Marshal(updatedAlert)
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	w.Write(response)
}

func alertsHandler(w http.ResponseWriter, r *http.Request, deps *HandlersDependencies) {
	switch r.Method {
	case "GET":
		getAlertsHandler(w, r, deps)
	case "POST":
		postAlertsHandler(w, r, deps)
	case "OPTIONS":
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.WriteHeader(http.StatusOK)
	case "PATCH":
		patchAlertsHandler(w, r, deps)
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func getAlertsLocationsHandler(w http.ResponseWriter, r *http.Request, deps *HandlersDependencies) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PATCH")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	client := deps.mongoClient
	collection := client.Database("fer-fall-detect").Collection("alerts")

	// Query the MongoDB database to retrieve all alerts with resolved = false
	filter := bson.M{"resolved": false}
	//cursor, err := collection.Find(context.Background(), bson.M{})
	cursor, err := collection.Find(context.Background(), filter)
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	defer cursor.Close(context.Background())

	// Store the latitudes and longitudes in a slice of slices
	latLongs := [][]float64{}
	for cursor.Next(context.Background()) {
		var alert AlertMsg
		if err := cursor.Decode(&alert); err != nil {
			log.Println(err)
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		lat, err := strconv.ParseFloat(alert.Latitude, 64)
		if err != nil {
			log.Println(err)
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		long, err := strconv.ParseFloat(alert.Longitude, 64)
		if err != nil {
			log.Println(err)
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		latLongs = append(latLongs, []float64{lat, long})
	}
	if err := cursor.Err(); err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Encode the slice of latitudes and longitudes as JSON
	jsonBytes, err := json.Marshal(latLongs)
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	// Write the JSON response back to the client
	w.WriteHeader(http.StatusOK)
	w.Write(jsonBytes)
}

func alertsLocationsHandler(w http.ResponseWriter, r *http.Request, deps *HandlersDependencies) {
	switch r.Method {
	case "GET":
		getAlertsLocationsHandler(w, r, deps)
	case "OPTIONS":
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.WriteHeader(http.StatusOK)
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func ignoreWatchMsg(requestBody map[string]interface{}) bool {
	data, ok := requestBody["data"].(map[string]interface{})
	if !ok {
		return false
	}
	content, ok := data["content"].(string)
	if !ok {
		return false
	}
	if !strings.HasPrefix(content, "SOS!") {
		return false
	}
	return true
}

func isWatchMsg(requestBody map[string]interface{}) bool {
	if requestBody["type"] == "message.phone.received" {
		return true
	}
	return false
}

func isNotebookMsg(requestBody map[string]interface{}) bool {
	if requestBody["source_type"] == "notebook" {
		return true
	}
	return false
}

func parseNotebookMsg(requestBody map[string]interface{}, alert *AlertMsg) {
	alert.SourceType = requestBody["source_type"].(string)
	alert.SourceID = requestBody["source_id"].(string)
	alert.Longitude = requestBody["longitude"].(string)
	alert.Latitude = requestBody["latitude"].(string)
	alert.Timestamp = requestBody["timestamp"].(string)
	alert.Comment = ""
	alert.Resolved = false
}

func parseWatchMsg(requestBody map[string]interface{}, alert *AlertMsg) {
	fmt.Println(requestBody)
	content := requestBody["data"].(map[string]interface{})["content"].(string)
	//re := regexp.MustCompile(`q=([\d\.]+),([\d\.]+)`)
	re := regexp.MustCompile(`q=(-?[\d\.]+),(-?[\d\.]+)`)
	match := re.FindStringSubmatch(content)
	latitude := ""
	longitude := ""
	if match != nil {
		latitude = match[1]
		longitude = match[2]
	}
	alert.SourceType = "watch"
	alert.SourceID = requestBody["data"].(map[string]interface{})["owner"].(string)
	alert.Longitude = longitude
	alert.Latitude = latitude
	alert.Timestamp = requestBody["data"].(map[string]interface{})["timestamp"].(string)
	alert.Comment = ""
	alert.Resolved = false
}

func publishToRedis(deps *HandlersDependencies, channelName string, message []byte) error {

	client := deps.redisClient
	// Publish the message to the channel
	fmt.Println("Publishing message: ", string(message))
	err := client.Publish(context.Background(), channelName, message).Err()
	if err != nil {
		return err
	}
	return nil
}

func insertAlertInMongo(deps *HandlersDependencies, alert *AlertMsg) error {
	client := deps.mongoClient
	collection := client.Database("fer-fall-detect").Collection("alerts")
	doc, err := collection.InsertOne(context.Background(), alert)
	if err != nil {
		return err
	}
	alert.Id = doc.InsertedID.(primitive.ObjectID)
	fmt.Println("Inserted document: ", alert)
	return nil
}

func postAlertsHandler(w http.ResponseWriter, r *http.Request, deps *HandlersDependencies) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS,PATCH")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	var requestBody map[string]interface{}
	var alert AlertMsg

	rb := r.Body

	err := json.NewDecoder(rb).Decode(&requestBody)
	if err != nil {
		fmt.Println("Bad Request - Not valid JSON")
		http.Error(w, "Bad Request - Not valid JSON", http.StatusBadRequest)
		return
	}

	if ignoreWatchMsg(requestBody) {
		fmt.Println("Info - Not important msg from watch, ignored it")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Info - Not important msg from watch, ignored it"))
		return
	} else {
		if isWatchMsg(requestBody) {
			fmt.Println("Info - Msg from watch")
			parseWatchMsg(requestBody, &alert)
		} else if isNotebookMsg(requestBody) {
			fmt.Println("Info - Msg from notebook")
			parseNotebookMsg(requestBody, &alert)
		} else {
			fmt.Println("Bad Request - Request body not valid")
			http.Error(w, "Bad Request - Request body not valid", http.StatusBadRequest)
			return
		}
	}

	// Save the alert to MongoDB
	err = insertAlertInMongo(deps, &alert)
	if err != nil {
		log.Println(err)
		http.Error(w, "Error saving alert to MongoDB", http.StatusInternalServerError)
		return
	}

	// Serialize the alert as a JSON string
	jsonBytes, err := json.Marshal(alert)
	if err != nil {
		log.Println(err)
		http.Error(w, "Error serializing alert", http.StatusInternalServerError)
		return
	}

	//Publish the alert to the channel
	err = publishToRedis(deps, "alerts", jsonBytes)
	if err != nil {
		log.Println(err)
		http.Error(w, "Error publishing alert to Redis", http.StatusInternalServerError)
		return
	}

	// Return the created resource to the caller
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(alert)

}

func alertsHandlerFunc(deps *HandlersDependencies) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		alertsHandler(w, r, deps)
	}
}

func alertsLocationsHandlerFunc(deps *HandlersDependencies) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		alertsLocationsHandler(w, r, deps)
	}
}

func main() {
	// start the server

	// FFD_MONGO_HOST := os.Getenv("FFD_MONGO_HOST")
	// FFD_MONGO_PORT := os.Getenv("FFD_MONGO_PORT")
	// FFD_MONGO_USER := os.Getenv("FFD_MONGO_USER")
	// FFD_MONGO_PASSWORD := os.Getenv("FFD_MONGO_PASSWORD")
	// FFD_REDIS_HOST := os.Getenv("FFD_REDIS_HOST")
	// FFD_REDIS_PORT := os.Getenv("FFD_REDIS_PORT")

	// if FFD_MONGO_HOST == "" || FFD_MONGO_PORT == "" || FFD_MONGO_USER == "" || FFD_MONGO_PASSWORD == "" || FFD_REDIS_HOST == "" || FFD_REDIS_PORT == "" {
	// 	log.Fatal("Error - Environment variables not set")
	// 	return
	// }

	redisClient, err := getRedisClient()
	if err != nil {
		log.Fatal(err)
		return
	}
	mongoClient, err := getMongoClient()
	if err != nil {
		log.Fatal(err)
		return
	}

	deps := &HandlersDependencies{
		redisClient: redisClient,
		mongoClient: mongoClient,
	}

	http.HandleFunc("/alerts", alertsHandlerFunc(deps))
	http.HandleFunc("/alertslocations", alertsLocationsHandlerFunc(deps))

	log.Fatal(http.ListenAndServe("0.0.0.0:6500", nil))
}
