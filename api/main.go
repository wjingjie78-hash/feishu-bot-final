package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
	"strings"
)

func Handler(w http.ResponseWriter, r *http.Request) {
	body, _ := ioutil.ReadAll(r.Body)
	content := string(body)

	// 如果飞书发来了 challenge 暗号，我们就把它原样返回去
	if strings.Contains(content, "challenge") {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, content)
		return
	}

	fmt.Fprintf(w, "Hello! Bot is alive!")
}

func main() {
	http.HandleFunc("/", Handler)
	http.ListenAndServe(":8080", nil)
}
