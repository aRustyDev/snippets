from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Header
from textual.containers import Horizontal
from textual.reactive import reactive

class ContainerFooterApp(App):
    """For complex footers with multiple child widgets, use container-based layouts rather than extending Footer directly. This provides better control over content flow"""
  
    CSS = """
    #footer-container {
        dock: bottom;
        height: 1;
        overflow-x: hidden;
        layout: grid;
        grid-columns: 1fr auto;
    }
    
    #footer-left {
        width: 75%;
        overflow-x: hidden;
    }
    
    #status-label {
        width: 25%;
        text-align: right;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Horizontal(id="footer-container"):
            yield Footer(id="footer-left")
            yield Label("Status: Ready", id="status-label")

class DynamicFooter(Container):
    """Dynamic content management requires reactive updates that maintain overflow control"""
  
    status = reactive("Ready")
    
    def compose(self) -> ComposeResult:
        yield Footer()
        yield Label(self.status, id="status")
    
    def watch_status(self, status: str) -> None:
        """Update status while maintaining overflow control."""
        status_label = self.query_one("#status", Label)
        status_label.update(status)
      
class EnhancedFooter(Container):
    """For custom footer widgets that extend functionality while preventing overflow, use the container composition pattern"""
  
    DEFAULT_CSS = """
    EnhancedFooter {
        dock: bottom;
        height: 3;
        overflow-x: hidden;
        layout: horizontal;
    }
    
    EnhancedFooter Footer {
        width: 1fr;
        overflow-x: hidden;
    }
    
    .status-section {
        width: auto;
        max-width: 25%;
        text-overflow: ellipsis;
        overflow: hidden;
        text-align: right;
        margin-left: 1;
    }
    """
    
    def __init__(self, status_text: str = "Ready"):
        super().__init__()
        self.status_text = status_text
    
    def compose(self) -> ComposeResult:
        yield Footer()
        yield Label(self.status_text, classes="status-section")

class NoScrollFooterApp(App):
    """Enhanced and container based version of a Footer(), it wraps a footer and splits Footer Extensions into sibling containers"""
  
    CSS = """
    #main-footer {
        dock: bottom;
        height: 3;
        overflow-x: hidden;
        overflow-y: hidden;
        layout: grid;
        grid-columns: 2fr 1fr;
    }
    
    #footer-keys {
        overflow-x: hidden;
        min-width: 0;
    }
    
    #footer-status {
        text-align: right;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        padding-right: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit Application"),
        ("ctrl+s", "save", "Save Current File"),
        ("ctrl+o", "open", "Open File"),
        ("f1", "help", "Show Help Dialog"),
    ]
    
    status = reactive("Ready")
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal(id="main-footer"):
            yield Footer(id="footer-keys")
            yield Label(self.status, id="footer-status")
    
    def on_mount(self) -> None:
        self.status = "Application loaded successfully"

if __name__ == "__main__":
    app = NoScrollFooterApp()
    app.run()
