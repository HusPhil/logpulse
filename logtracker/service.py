import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import os
import logging
from logtracker.main import main, stop_event

class LogTrackerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "LogTracker"
    _svc_display_name_ = "LogTracker Activity Logger"
    _svc_description_ = "Background service for periodic activity logging"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        
        # Set up logging
        if not os.path.exists('logs'):
            os.makedirs('logs')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/service.log'),
            ]
        )
        self.logger = logging.getLogger(__name__)

    def SvcStop(self):
        """Stop the service."""
        self.logger.info("Service stop requested")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        stop_event.set()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """Run the service."""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.logger.info("LogTracker service started")
        
        try:
            # Run main application in service mode
            main(as_service=True)
        except Exception as e:
            self.logger.error(f"Service error: {e}")
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_ERROR_TYPE,
                servicemanager.PYS_SERVICE_STOPPED,
                (self._svc_name_, str(e))
            )

def install_service():
    """Install the service."""
    try:
        win32serviceutil.InstallService(
            LogTrackerService,
            LogTrackerService._svc_name_,
            LogTrackerService._svc_display_name_,
            startType=win32service.SERVICE_AUTO_START,
            description=LogTrackerService._svc_description_
        )
        print(f"Service '{LogTrackerService._svc_display_name_}' installed successfully")
        print("Service will start automatically on boot")
        return True
    except Exception as e:
        print(f"Failed to install service: {e}")
        return False

def remove_service():
    """Remove the service."""
    try:
        win32serviceutil.RemoveService(LogTrackerService._svc_name_)
        print(f"Service '{LogTrackerService._svc_display_name_}' removed successfully")
        return True
    except Exception as e:
        print(f"Failed to remove service: {e}")
        return False

def start_service():
    """Start the service."""
    try:
        win32serviceutil.StartService(LogTrackerService._svc_name_)
        print(f"Service '{LogTrackerService._svc_display_name_}' started successfully")
        return True
    except Exception as e:
        print(f"Failed to start service: {e}")
        return False

def stop_service():
    """Stop the service."""
    try:
        win32serviceutil.StopService(LogTrackerService._svc_name_)
        print(f"Service '{LogTrackerService._svc_display_name_}' stopped successfully")
        return True
    except Exception as e:
        print(f"Failed to stop service: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(LogTrackerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(LogTrackerService)