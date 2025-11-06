import os
import shutil
from datetime import datetime
import json

class MacroPrankMitigator:
    """Automatically cleans up macro prank artifacts"""
    
    def __init__(self, target_path):
        self.target_path = target_path
        self.removed_files = []
        self.removed_folders = []
        self.quarantine_folder = os.path.join(
            os.path.expanduser("~"), 
            "Desktop", 
            "Quarantine_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        )
        
    def scan_for_threats(self):
        """Scan for prank artifacts"""
        print("🔍 Scanning for macro prank artifacts...\\n")
        
        threats = {
            'suspicious_folders': [],
            'suspicious_files': []
        }
        
        # Scan for suspicious folders
        for item in os.listdir(self.target_path):
            item_path = os.path.join(self.target_path, item)
            
            if os.path.isdir(item_path):
                # Check for prank folder patterns
                if any(keyword in item.lower() for keyword in 
                      ['maze', 'surprise', 'mystery', 'level', 'oops', 'whoops']):
                    threats['suspicious_folders'].append(item_path)
            
            elif os.path.isfile(item_path):
                # Check for prank file patterns
                if any(keyword in item.lower() for keyword in 
                      ['pranked', 'gotcha', 'surprise']):
                    threats['suspicious_files'].append(item_path)
        
        return threats
    
    def display_threats(self, threats):
        """Display found threats"""
        total = len(threats['suspicious_folders']) + len(threats['suspicious_files'])
        
        if total == 0:
            print("✅ No threats detected!\\n")
            return False
        
        print(f"⚠️  Found {total} suspicious items:\\n")
        
        if threats['suspicious_folders']:
            print(f"📁 Suspicious Folders ({len(threats['suspicious_folders'])}):")
            for folder in threats['suspicious_folders'][:10]:
                print(f"   - {os.path.basename(folder)}")
            if len(threats['suspicious_folders']) > 10:
                print(f"   ... and {len(threats['suspicious_folders']) - 10} more")
        
        if threats['suspicious_files']:
            print(f"\\n📄 Suspicious Files ({len(threats['suspicious_files'])}):")
            for file in threats['suspicious_files'][:10]:
                print(f"   - {os.path.basename(file)}")
            if len(threats['suspicious_files']) > 10:
                print(f"   ... and {len(threats['suspicious_files']) - 10} more")
        
        print()
        return True
    
    def quarantine_item(self, item_path):
        """Move item to quarantine folder"""
        if not os.path.exists(self.quarantine_folder):
            os.makedirs(self.quarantine_folder)
        
        item_name = os.path.basename(item_path)
        quarantine_path = os.path.join(self.quarantine_folder, item_name)
        
        try:
            shutil.move(item_path, quarantine_path)
            return True
        except Exception as e:
            print(f"   ❌ Error moving {item_name}: {e}")
            return False
    
    def delete_item(self, item_path):
        """Permanently delete item"""
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                self.removed_folders.append(item_path)
            else:
                os.remove(item_path)
                self.removed_files.append(item_path)
            return True
        except Exception as e:
            print(f"   ❌ Error deleting {os.path.basename(item_path)}: {e}")
            return False
    
    def mitigate(self, action='quarantine'):
        """Execute mitigation"""
        threats = self.scan_for_threats()
        
        if not self.display_threats(threats):
            return
        
        print(f"🛡️  Starting mitigation (Action: {action})...\\n")
        
        all_threats = threats['suspicious_folders'] + threats['suspicious_files']
        
        for item in all_threats:
            item_name = os.path.basename(item)
            
            if action == 'quarantine':
                if self.quarantine_item(item):
                    print(f"   ✅ Quarantined: {item_name}")
                    if os.path.isdir(item):
                        self.removed_folders.append(item)
                    else:
                        self.removed_files.append(item)
            
            elif action == 'delete':
                if self.delete_item(item):
                    print(f"   ✅ Deleted: {item_name}")
        
        self.generate_report()
    
    def generate_report(self):
        """Generate mitigation report"""
        print("\\n" + "="*60)
        print("📊 MITIGATION REPORT")
        print("="*60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\\nFiles removed: {len(self.removed_files)}")
        print(f"Folders removed: {len(self.removed_folders)}")
        
        if os.path.exists(self.quarantine_folder):
            print(f"\\nQuarantined items location:")
            print(f"  {self.quarantine_folder}")
        
        print("\\n✅ Mitigation complete!")
        print("="*60 + "\\n")
        
        # Save report
        report_file = "mitigation_report.txt"
        with open(report_file, "w") as f:
            f.write(f"Mitigation Report - {datetime.now()}\\n")
            f.write("="*60 + "\\n")
            f.write(f"Files removed: {len(self.removed_files)}\\n")
            f.write(f"Folders removed: {len(self.removed_folders)}\\n")
            f.write("\\nRemoved items:\\n")
            for item in self.removed_files + self.removed_folders:
                f.write(f"  - {item}\\n")
        
        print(f"📄 Detailed report saved to: {report_file}")

def main():
    """Main mitigation interface"""
    print("="*60)
    print("🛡️  MACRO PRANK MITIGATION TOOL")
    print("="*60)
    print()
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    mitigator = MacroPrankMitigator(desktop_path)
    
    # Scan first
    threats = mitigator.scan_for_threats()
    found_threats = mitigator.display_threats(threats)
    
    if not found_threats:
        return
    
    print("Choose action:")
    print("  1. Quarantine (move to safe folder)")
    print("  2. Delete permanently")
    print("  3. Cancel")
    
    choice = input("\\nEnter choice (1-3): ")
    
    if choice == '1':
        mitigator.mitigate(action='quarantine')
    elif choice == '2':
        confirm = input("⚠️  Are you sure? This cannot be undone (y/n): ")
        if confirm.lower() == 'y':
            mitigator.mitigate(action='delete')
        else:
            print("Cancelled.")
    else:
        print("Cancelled.")

if __name__ == "__main__":
    main()
