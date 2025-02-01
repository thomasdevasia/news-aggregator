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

type newsPayload struct {
	Action   string   `json:"action"`
	NewsItem NewsItem `json:"news"`
}

func sendNews(newsItems []NewsItem, userName string) (string, error) {
	// Send the newsItems to the user
	// This is a placeholder for the actual implementation
	const userService = "http://user-service:8002"
	for _, newsItem := range newsItems {
		jsonPayload, err := json.Marshal(newsPayload{Action: "save", NewsItem: newsItem})
		if err != nil {
			return "", errors.New("error marshalling payload")
		}
		req, err := http.NewRequest("POST", fmt.Sprintf("%s/%s/news", userService, userName), bytes.NewBuffer(jsonPayload))
		if err != nil {
			log.Printf("error creating request to user-service: %s", err)
			return "", errors.New("error creating request to user-service")
		}
		req.Header.Set("Content-Type", "application/json")
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			log.Printf("error making request to user-service: %s", err)
			return "", errors.New("error making request to user-service")
		}
		if resp.StatusCode != http.StatusOK {
			log.Printf("error sending news: %s", resp.Status)
			body, _ := io.ReadAll(resp.Body)
			log.Printf("response body: %s", string(body))
		} else {
			log.Printf("news sent to %s", userName)
		}
		defer resp.Body.Close()
	}

	return "News sent", nil
}
