import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

class MacroPrankDetector(FileSystemEventHandler):
    """Detects and responds to macro prank activity"""
    
    def __init__(self, watch_path):
        self.watch_path = watch_path
        self.file_creates = []
        self.folder_creates = []
        self.start_time = time.time()
        self.alert_threshold = 5  # Alert if 5+ files/folders in 10 seconds
        self.log_file = "security_log.txt"
        
    def log_event(self, message):
        """Log security events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\\n"
        print(log_entry.strip())
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)
    
    def on_created(self, event):
        current_time = time.time()
        
        if event.is_directory:
            self.folder_creates.append({
                'path': event.src_path,
                'time': current_time
            })
            self.log_event(f"FOLDER CREATED: {event.src_path}")
        else:
            self.file_creates.append({
                'path': event.src_path,
                'time': current_time
            })
            self.log_event(f"FILE CREATED: {event.src_path}")
        
        # Check for suspicious activity
        self.check_for_threats()
    
    def check_for_threats(self):
        """Analyze patterns for macro prank behavior"""
        current_time = time.time()
        time_window = 10  # seconds
        
        # Count recent file creates
        recent_files = [f for f in self.file_creates 
                       if current_time - f['time'] < time_window]
        
        # Count recent folder creates
        recent_folders = [f for f in self.folder_creates 
                         if current_time - f['time'] < time_window]
        
        # Detect nested folder pattern (Level1, Level2, etc.)
        nested_pattern = any('Level' in f['path'] for f in recent_folders)
        
        # Detect prank file names
        prank_pattern = any('pranked' in f['path'] or 'file' in f['path'].lower() 
                          for f in recent_files)
        
        # Calculate threat score
        threat_score = 0
        threats = []
        
        if len(recent_files) > self.alert_threshold:
            threat_score += 3
            threats.append(f"Mass file creation: {len(recent_files)} files in {time_window}s")
        
        if len(recent_folders) > self.alert_threshold:
            threat_score += 3
            threats.append(f"Mass folder creation: {len(recent_folders)} folders in {time_window}s")
        
        if nested_pattern:
            threat_score += 2
            threats.append("Nested folder pattern detected (Level1, Level2...)")
        
        if prank_pattern:
            threat_score += 2
            threats.append("Suspicious file naming pattern detected")
        
        # Alert if threat detected
        if threat_score >= 3:
            self.trigger_alert(threat_score, threats, recent_files, recent_folders)
    
    def trigger_alert(self, score, threats, files, folders):
        """Trigger security alert"""
        print("\\n" + "="*60)
        print("🚨 SECURITY ALERT: MACRO PRANK DETECTED!")
        print("="*60)
        print(f"Threat Score: {score}")
        print(f"\\nThreats Identified:")
        for threat in threats:
            print(f"  - {threat}")
        
        print(f"\\nRecent Activity:")
        print(f"  Files created: {len(files)}")
        print(f"  Folders created: {len(folders)}")
        
        print("\\nSample paths:")
        for f in files[:3]:
            print(f"  FILE: {f['path']}")
        for f in folders[:3]:
            print(f"  FOLDER: {f['path']}")
        
        print("\\n⚠️  RECOMMENDATION: Run mitigation script immediately!")
        print("="*60 + "\\n")
        
        # Auto-trigger mitigation (optional)
        response = input("Run automatic mitigation? (y/n): ")
        if response.lower() == 'y':
            print("Launching mitigation...")
            os.system("python mitigation.py")

def start_monitoring(path):
    """Start the monitoring service"""
    print("="*60)
    print("🛡️  MACRO PRANK DEFENSE SYSTEM ACTIVATED")
    print("="*60)
    print(f"Monitoring: {path}")
    print(f"Log file: security_log.txt")
    print("Press Ctrl+C to stop\\n")
    
    event_handler = MacroPrankDetector(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n\\nStopping monitor...")
        observer.stop()
    observer.join()
    print("Monitor stopped.")

if __name__ == "__main__":
    # Monitor the Desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    start_monitoring(desktop_path)
