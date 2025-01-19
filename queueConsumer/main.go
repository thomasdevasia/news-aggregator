package main

import (
	"fmt"
	"log"
	"os"

	amqp "github.com/rabbitmq/amqp091-go"
)

type QueueConsumer struct {
	conn      *amqp.Connection
	channel   *amqp.Channel
	queueName string
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func NewQueueConsumer(amqpURL, queueName string) *QueueConsumer {
	conn, err := amqp.Dial(amqpURL)
	failOnError(err, "Failed to connect to RabbitMQ")

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")

	_, err = ch.QueueDeclare(
		queueName,
		true,
		true,
		false,
		false,
		nil,
	)
	failOnError(err, "Failed to declare a queue")

	return &QueueConsumer{
		conn:      conn,
		channel:   ch,
		queueName: queueName,
	}
}

func (consumer *QueueConsumer) Close() {
	consumer.channel.Close()
	consumer.conn.Close()
}

func (consumer *QueueConsumer) Consume() <-chan amqp.Delivery {
	messages, err := consumer.channel.Consume(
		consumer.queueName,
		"",
		true,
		false,
		false,
		false,
		nil,
	)

	failOnError(err, "Failed to register a consumer")

	return messages
}

func main() {
	amqpURL := fmt.Sprintf("amqp://%s:%s@rabbitmq:5672/", os.Getenv("RABBITMQ_USER"), os.Getenv("RABBITMQ_PASS"))
	queueName := "user.newsCollection"
	fmt.Println("amqpURL: ", amqpURL)
	fmt.Println("queueName: ", queueName)

	consumer := NewQueueConsumer(amqpURL, queueName)
	defer consumer.Close()

	forever := make(chan struct{})

	messages := consumer.Consume()

	go func() {
		for message := range messages {
			log.Printf("Received a message: %s", message.Body)
		}
	}()

	fmt.Println(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever
}
