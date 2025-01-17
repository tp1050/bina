let scannedData = [];
let isScanning = false;

document.addEventListener('DOMContentLoaded', () => {
    loadSavedScans();
    
    document.getElementById('scanButton').addEventListener('click', () => {
        if (!isScanning) {
            performScan();
        }
    });

    document.getElementById('backButton').addEventListener('click', () => {
        document.getElementById('main-view').style.display = 'block';
        document.getElementById('detail-view').style.display = 'none';
    });
});

function loadSavedScans() {
    // Load saved scans from localStorage
    const saved = localStorage.getItem('scannedData');
    if (saved) {
        scannedData = JSON.parse(saved);
        updateJsonList();
    }
}

function performScan() {
    isScanning = true;
    
    // Simulate scanning process
    const newScan = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        data: { /* Your scan data here */ }
    };
    
    scannedData.push(newScan);
    localStorage.setItem('scannedData', JSON.stringify(scannedData));
    updateJsonList();
    
    isScanning = false;
}

function updateJsonList() {
    const listElement = document.getElementById('jsonList');
    listElement.innerHTML = '';
    
    scannedData.forEach(scan => {
        const div = document.createElement('div');
        div.className = 'json-item';
        div.textContent = `Scan from ${new Date(scan.timestamp).toLocaleString()}`;
        div.onclick = () => showJsonDetail(scan);
        listElement.appendChild(div);
    });
}

function showJsonDetail(scan) {
    document.getElementById('main-view').style.display = 'none';
    document.getElementById('detail-view').style.display = 'block';
    document.getElementById('jsonContent').textContent = JSON.stringify(scan, null, 2);
}
