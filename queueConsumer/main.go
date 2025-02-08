package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"
)

func main() {
	amqpURL := fmt.Sprintf("amqp://%s:%s@rabbitmq:5672/", os.Getenv("RABBITMQ_USER"), os.Getenv("RABBITMQ_PASS"))
	queueName := "user.newsCollection"
	fmt.Println("amqpURL: ", amqpURL)
	fmt.Println("queueName: ", queueName)

	// just giving time for rabbitmq to start
	time.Sleep(30 * time.Second)
	log.Printf("Connecting to RabbitMQ at %s", amqpURL)

	consumer := NewQueueConsumer(amqpURL, queueName)
	defer consumer.Close()

	forever := make(chan struct{})

	messages := consumer.Consume()

	go func() {
		for message := range messages {
			log.Printf("Received a message: %s", message.Body)
			var msg Message
			err := json.Unmarshal(message.Body, &msg)
			if err != nil {
				log.Printf("Error decoding JSON: %s", err)
				continue
			}
			// log.Printf("user_id: %d", msg.User_id)
			// log.Printf("topics: %v", msg.Topics)
			payload := Payload{Topics: msg.Topics}
			// log.Printf("payload: %v", payload)
			resp, err := RequestNewsCollection(payload)
			log.Printf("Got %d news back", len(resp))
			if err != nil {
				log.Printf("Error requesting news collection: %s", err)
				continue
			}
			// log.Printf("Response: %s", resp)
			_, err = sendNews(resp, msg.UserName)
			if err != nil {
				log.Printf("Error sending news: %s", err)
				continue
			}
			// log.Printf("Response: %s", resp)
		}
	}()

	fmt.Println(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever
}
