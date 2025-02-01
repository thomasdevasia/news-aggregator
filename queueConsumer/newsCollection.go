package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
)

type Payload struct {
	Topics []string `json:"topics"`
}

type NewsItem struct {
	Source   string `json:"source"`
	Heading  string `json:"heading"`
	NewsType string `json:"newsType"`
	Datetime string `json:"datetime"`
	Data     string `json:"data"`
}

func RequestNewsCollection(payload Payload) ([]NewsItem, error) {
	collectionService := "http://news-collection:3001"

	errorNews := []NewsItem{}

	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		return errorNews, errors.New("error marshalling payload")
	}
	// log.Printf("jsonPayload: %s", string(jsonPayload))

	// resp, err := http.Post("http://news-collection:3001/getNews", "application/json", bytes.NewBuffer(jsonPayload))
	req, err := http.NewRequest("POST", fmt.Sprintf("%s/getNews", collectionService), bytes.NewBuffer(jsonPayload))
	if err != nil {
		log.Printf("error creating request to news-collection: %s", err)
		return errorNews, errors.New("error creating request to news-collection")
	}

	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}

	resp, err := client.Do(req)
	if err != nil {
		log.Printf("error making request to news-collection: %s", err)
		return errorNews, errors.New("error making request to news-collection")
	}

	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var newsItems []NewsItem
	err = json.Unmarshal(body, &newsItems)
	if err != nil {
		log.Printf("error unmarshalling response news-collection: %s", err)
		return errorNews, errors.New("error unmarshalling response")
	}

	// count := len(newsItems)
	// log.Printf("Received %d news items", count)
	// for _, newsItem := range newsItems {
	// 	log.Printf("Source: %s", newsItem.Source)
	// 	log.Printf("Heading: %s", newsItem.Heading)
	// 	log.Printf("NewsType: %s", newsItem.NewsType)
	// 	log.Printf("Datetime: %s", newsItem.Datetime)
	// 	log.Printf("Data: %s", newsItem.Data)
	// 	log.Printf("---")
	// }
	//
	return newsItems, nil
}
