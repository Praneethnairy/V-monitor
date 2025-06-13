package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"path/filepath"
)

type Response struct {
	Status  string      `json:"status"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
}

func runPythonScript(scriptPath string) ([]byte, error) {
	cmd := exec.Command("sudo", "python3", scriptPath)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("script error: %v, output: %s", err, string(output))
	}
	return output, nil
}

func getHostMetrics(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	scriptPath := filepath.Join("..", "V-monitor-core", "HostMonitoring.py")
	output, err := runPythonScript(scriptPath)
	if err != nil {
		response := Response{
			Status:  "error",
			Message: fmt.Sprintf("Error running host monitoring: %v", err),
		}
		json.NewEncoder(w).Encode(response)
		return
	}

	var data interface{}
	if err := json.Unmarshal(output, &data); err != nil {
		response := Response{
			Status:  "error",
			Message: fmt.Sprintf("Error parsing host metrics: %v", err),
		}
		json.NewEncoder(w).Encode(response)
		return
	}

	response := Response{
		Status: "success",
		Data:   data,
	}
	json.NewEncoder(w).Encode(response)
}

func getContainerMetrics(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	scriptPath := filepath.Join("..", "V-monitor-core", "ContainerMonitoring.py")
	output, err := runPythonScript(scriptPath)
	if err != nil {
		response := Response{
			Status:  "error",
			Message: fmt.Sprintf("Error running container monitoring: %v", err),
		}
		json.NewEncoder(w).Encode(response)
		return
	}

	var data interface{}
	if err := json.Unmarshal(output, &data); err != nil {
		response := Response{
			Status:  "error",
			Message: fmt.Sprintf("Error parsing container metrics: %v", err),
		}
		json.NewEncoder(w).Encode(response)
		return
	}

	response := Response{
		Status: "success",
		Data:   data,
	}
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/api/host", getHostMetrics)
	http.HandleFunc("/api/containers", getContainerMetrics)

	port := ":8080"
	fmt.Printf("Server starting on port %s...\n", port)
	if err := http.ListenAndServe(port, nil); err != nil {
		log.Fatal(err)
	}
} 