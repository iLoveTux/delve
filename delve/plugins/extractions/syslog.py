import re
import logging

pattern = re.compile(r"^(?P<month>\w+)\s+(?P<day>\d+)\s+(?P<time>\d+:\d+:\d+)\s+(?P<hostname>.*?)\s+(?P<executable>.*?):(?P<message>.*)$")

def syslog(event):
    log = logging.getLogger(__name__)
    log.debug(f"Extracting syslog fields from event: '{event}'")
    if match := pattern.search(event):
        log.debug("Matches pattern")
        return match.groupdict()
    return {}
