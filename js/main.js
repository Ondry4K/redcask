// p.s. some of this is not my work, i simply cba to learn a whole new programming language for the backend of my web-ui
// UI Update Functions for RedCask
var serverKey = ""; // Store the key globally for later use
var base = window.location.origin;

// Function to save key to localStorage
function saveKey(key) {
    localStorage.setItem('redcask_server_key', key);
}

// Function to get key from localStorage
function getSavedKey() {
    return localStorage.getItem('redcask_server_key');
}

// Function to clear saved key
function clearSavedKey() {
    localStorage.removeItem('redcask_server_key');
}

// Function to validate key (can be called with a key parameter or use input)
function validateKey(keyToValidate = null) {
    var key = keyToValidate || document.getElementById("server-key").value;
    if (key === "") {
        alert("Please enter a server key.");
        return;
    }
    
    fetch(base + "/validate_key", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "Authorization": key })
    })
    .then(response => response.text())
    .then(text => {
        console.log("Validation response:", text); // Debug log
        const data = text === "true" ? true : (text === "false" ? false : JSON.parse(text));
        if (data === true) {
            serverKey = key; // Store key globally
            saveKey(key); // Save to localStorage
            document.getElementById("app").style.display = "";
            document.getElementById("login").style.display = "none";
            
            // Load initial data
            loadAllData();
        } else {
            alert("Invalid server key. Please try again.");
            clearSavedKey(); // Clear invalid key from storage
        }
    })
    .catch(error => {
        console.error("Error validating key:", error);
        alert("Error connecting to server. Please try again.");
        clearSavedKey(); // Clear key on connection error
    });
}

// Function to auto-validate saved key on page load
function autoValidateKey() {
    const savedKey = getSavedKey();
    if (savedKey) {
        document.getElementById("server-key").value = savedKey; // Show saved key in input
        validateKey(savedKey); // Auto-validate
    }
}

// Updated validateKey function with proper UI updates
function validateKey() {
    var key = document.getElementById("server-key").value;
    if (key === "") {
        alert("Please enter a server key.");
        return;
    }
    
    fetch(base + "/validate_key", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "Authorization": key })
    })
    .then(response => response.text())
    .then(text => {
        console.log("Validation response:", text); // Debug log
        const data = text === "true" ? true : (text === "false" ? false : JSON.parse(text));
        if (data === true) {
            serverKey = key; // Store key globally
            document.getElementById("app").style.display = "";
            document.getElementById("login").style.display = "none";
            
            // Load initial data
            loadAllData();
        } else {
            alert("Invalid server key. Please try again.");
        }
    })
    .catch(error => {
        console.error("Error validating key:", error);
        alert("Error connecting to server. Please try again.");
    });
}

// Function to load all data (queue, status, devices)
function loadAllData() {
    loadQueue();
    loadStatus();
    loadDevices();
}

// Function to update queue UI
function loadQueue() {
    fetch(base + "/queue", {
        headers: {
            "Authorization": serverKey
        }
    })
    .then(response => response.json())
    .then(queueData => {
        updateQueueUI(queueData);
    })
    .catch(error => {
        console.error("Error fetching queue data:", error);
        updateQueueUI(null);
    });
}

// Function to update status UI
function loadStatus() {
    fetch(base + "/status", {
        headers: {
            "Authorization": serverKey
        }
    })
    .then(response => response.json())
    .then(statusData => {
        updateStatusUI(statusData);
    })
    .catch(error => {
        console.error("Error fetching status data:", error);
        updateStatusUI(null);
    });
}

// Function to load devices
function loadDevices() {
    fetch(base + "/devices", {
        headers: {
            "Authorization": serverKey
        }
    })
    .then(response => response.json())
    .then(deviceData => {
        updateDevicesUI(deviceData);
    })
    .catch(error => {
        console.error("Error fetching device data:", error);
        updateDevicesUI(null);
    });
}

// Function to update the queue UI
function updateQueueUI(queueData) {
    const queueList = document.getElementById("queue-list");
    
    if (!queueData || !queueData.queue || queueData.queue.length === 0) {
        queueList.innerHTML = "<li>No torrents in queue</li>";
        return;
    }
    
    queueList.innerHTML = "";
    queueData.queue.forEach(item => {
        const li = document.createElement("li");
        
        // Truncate magnet to first 16 characters
        const magnetDisplay = item.magnet_link.length > 16 
            ? item.magnet_link.substring(0, 16) + "..." 
            : item.magnet_link;
            
        li.innerHTML = `
            <strong>Device:</strong> ${item.uuid}<br>
            <strong>Magnet:</strong> ${magnetDisplay}<br>
            <button onclick="removeFromQueue('${item.uuid}', '${item.magnet_link}')" style="margin-left: 10px; color: red;">Remove</button>
        `;
        queueList.appendChild(li);
    });
}

// Function to update the status UI
function updateStatusUI(statusData) {
    const statusList = document.getElementById("status-list");
    
    if (!statusData || statusData.length === 0) {
        statusList.innerHTML = "<li>No active torrents</li>";
        return;
    }
    
    statusList.innerHTML = "";
    statusData.forEach(item => {
        const li = document.createElement("li");
        
        li.innerHTML = `
            <strong>Name:</strong> ${item.name}<br>
            <strong>Device:</strong> ${item.uuid}<br>
            <strong>Progress:</strong> ${item.progress.toFixed(1)}%<br>
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 2px; margin: 5px 0;">
                <div style="background-color: #4CAF50; height: 20px; border-radius: 8px; width: ${item.progress}%; min-width: 20px; text-align: center; color: white; line-height: 20px; font-size: 12px;">
                    ${item.progress.toFixed(1)}%
                </div>
            </div>
        `;
        statusList.appendChild(li);
    });
}

// Function to update the devices UI
function updateDevicesUI(deviceData) {
    const deviceList = document.getElementById("device-list");
    
    if (!deviceData || !deviceData.devices || deviceData.devices.length === 0) {
        deviceList.innerHTML = "<li>No devices registered</li>";
        return;
    }
    
    deviceList.innerHTML = "";
    deviceData.devices.forEach(device => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>UUID:</strong> ${device.uuid}<br>
            <strong>IP:</strong> ${device.ip}<br>
            <strong>Status:</strong> <span style="color: green;">Online</span>
        `;
        deviceList.appendChild(li);
    });
}

// Helper function to format bytes
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Function to remove torrent from queue
function removeFromQueue(uuid, magnetLink) {
    if (!confirm("Are you sure you want to remove this torrent from the queue?")) {
        return;
    }
    
    fetch(base + "/queue", {
        method: "DELETE",
        headers: {
            "Authorization": serverKey,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "uuid": uuid,
            "magnet_link": magnetLink
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
            loadQueue(); // Reload queue data
        } else {
            alert(data.detail || "Failed to remove torrent from queue");
        }
    })
    .catch(error => {
        console.error("Error removing torrent:", error);
        alert("Error removing torrent from queue");
    });
}

// Function to add torrent to queue
function addTorrent() {
    const magnetUrl = document.getElementById("magnet-url").value;
    const torrentFile = document.getElementById("torrent-file").files[0];
    const deviceUuid = document.getElementById("uuid").value;
    
    if (!magnetUrl && !torrentFile) {
        alert("Please enter a magnet URL or select a torrent file");
        return;
    }
    
    if (!deviceUuid) {
        alert("Please enter a device UUID");
        return;
    }
    
    let torrentData;
    if (magnetUrl) {
        torrentData = magnetUrl;
    } else {
        // Handle file upload - you'll need to read the file
        const reader = new FileReader();
        reader.onload = function(e) {
            const fileContent = e.target.result;
            sendAddTorrentRequest(deviceUuid, fileContent);
        };
        reader.readAsText(torrentFile);
        return;
    }
    
    sendAddTorrentRequest(deviceUuid, torrentData);
}

// Helper function to send add torrent request
function sendAddTorrentRequest(deviceUuid, magnetLink) {
    fetch(base + "/queue", {
        method: "POST",
        headers: {
            "Authorization": serverKey,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "uuid": deviceUuid,
            "magnet_link": magnetLink
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
            document.getElementById("magnet-url").value = "";
            document.getElementById("torrent-file").value = "";
            document.getElementById("uuid").value = "";
            loadQueue(); // Reload queue data
        } else {
            alert(data.detail || "Failed to add torrent to queue");
        }
    })
    .catch(error => {
        console.error("Error adding torrent:", error);
        alert("Error adding torrent to queue");
    });
}

// Function to logout
function logout() {
    document.getElementById("login").style.display = "";
    document.getElementById("app").style.display = "none";
    document.getElementById("server-key").value = "";
    serverKey = "";
    clearSavedKey(); // Clear saved key on logout
}

// Auto-refresh data every 5 seconds when logged in
setInterval(() => {
    if (serverKey && document.getElementById("app").style.display !== "none") {
        loadStatus(); // Only refresh status as it changes most frequently
    }
}, 5000);

// Event listeners
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("login-btn").addEventListener("click", () => validateKey());
    document.getElementById("logout-btn").addEventListener("click", logout);
    document.getElementById("add-torrent-btn").addEventListener("click", addTorrent);
    
    // Allow Enter key to login
    document.getElementById("server-key").addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            validateKey();
        }
    });
    
    // Auto-validate saved key on page load
    autoValidateKey();
});
