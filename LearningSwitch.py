



from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time

log = core.getLogger()




class LearningSwitch (object):

  def __init__ (self, connection):
    
    self.connection = connection
    
    
    self.MacAdresiPortAdresi = {}

    
    connection.addListeners(self)

    
    

   

  def _handle_PacketIn (self, event):
    
    #YENi PAKET geldi kontrol elemanina
    packet = event.parsed

    def flood (message = None):
      #paketi tum portlara gonderme fonksiyonu
      msg = of.ofp_packet_out()
      

      

      if message is not None: log.debug(message)
        
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      
        
      msg.data = event.ofp
      msg.in_port = event.port
      self.connection.send(msg)

    def drop (zaman = None):
      """
      Paketi at. Eger bir zaman verilmisse o zamanda gelen bu tur paketlerin hepsini at
      """
      if zaman is not None:
        if not isinstance(zaman, tuple):
          zaman = (zaman,zaman)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = zaman[0]
        msg.hard_timeout = zaman[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    self.MacAdresiPortAdresi[packet.src] = event.port # 1.. adim

    
    if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
        drop() 
        return

    if packet.dst.is_multicast:
      flood() # 3adim
    else:
      if packet.dst not in self.MacAdresiPortAdresi: # 4adim
        flood(" %s adresinin portu bilinmiyor  -- floodlaniyor" % (packet.dst,)) 
      else:
        port = self.MacAdresiPortAdresi[packet.dst]
        if port == event.port: # 5 adim
          
          log.warning("portlar ayni %s -> %s  %s.%s.  atildi."
              % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
          drop(10)
          return
        # 6 adim
        log.debug("akis girdisi ekleniyor %s.%i -> %s.%i" %
                  (packet.src, event.port, packet.dst, port))
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port = port))
        msg.data = event.ofp 
        self.connection.send(msg)


class learning (object):
  """
  Open flow switchlerinin baglanmasini bekleyerek onlari learning switche cevirir.
  """
  
  def __init__ (self):
    core.openflow.addListeners(self)
    

  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection)


def launch ():
  """
  Learning switch baslar
  """
  

  core.registerNew(learning)
