package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func Handler(w http.ResponseWriter, r *http.Request) {
	// 专门处理飞书的首次验证请求
	var data map[string]interface{}
	json.NewDecoder(r.Body).Decode(&data)
	
	if challenge, ok := data["challenge"]; ok {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, "{\"challenge\":\"%s\"}", challenge)
		return
	}
	
	fmt.Fprint(w, "Hello! Bot is running.")
}

func main() {
	http.HandleFunc("/", Handler)
	http.ListenAndServe(":8080", nil)
}
