package main

import (
	"log"

	amqp "github.com/rabbitmq/amqp091-go"
)

type QueueConsumer struct {
	conn      *amqp.Connection
	channel   *amqp.Channel
	queueName string
}

type Message struct {
	User_id int      `json:"user_id"`
	Topics  []string `json:"topics"`
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
