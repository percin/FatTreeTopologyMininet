
import pox.log
from pox.core import core
import pox.openflow.discovery
import pox.log.color
import LearningSwitch 
import pox.openflow.spanning_tree

def launch ():
  
  pox.log.color.launch()
  
  pox.log.launch(format="[@@@bold@@@level%(name)-22s@@@reset] " +
                        "@@@bold%(message)s@@@normal")
  core.getLogger("Kontrol elemani basladi").setLevel("INFO")
  pox.openflow.discovery.launch()
  pox.openflow.spanning_tree.launch()

  LearningSwitch.launch()

  
  