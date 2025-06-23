def process_signal(sender: str):
    domain = sender.split('@')[-1]
    if domain == "malicious.com":
        return "bad"
    else:
        return "good"
