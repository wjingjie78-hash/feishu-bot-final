package main

import (
	"fmt"
	"net/http"
	"io"
	"strings"
)

func Handler(w http.ResponseWriter, r *http.Request) {
	// 读取飞书发来的加密暗号
	body, _ := io.ReadAll(r.Body)
	content := string(body)

	w.Header().Set("Content-Type", "application/json")

	// 如果飞书在做地址验证，我们就把收到的内容原样吐回去
	if strings.Contains(content, "challenge") {
		fmt.Fprintf(w, content)
		return
	}

	// 否则显示机器人已经准备好了
	fmt.Fprintf(w, "{\"message\": \"robot_is_online\"}")
}

func main() {
	http.HandleFunc("/", Handler)
	http.ListenAndServe(":8080", nil)
}
