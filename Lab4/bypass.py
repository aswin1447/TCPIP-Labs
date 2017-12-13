from time import sleep
from pox.core import core
import pox.openflow.libopenflow_01 as of
"""
Complement to be used in Lab4
"""

from pox.lib.util import dpid_to_str
import time
from pox.openflow.discovery import Discovery
from pox.lib.addresses import IPAddr

log = core.getLogger()

lab4tools = {
'IP2': IPAddr("10.10.2.2"),
'IP3': IPAddr("10.10.3.3"),
'FlagSW2': True, 
'FlagSW3': True, 
'SW2dpid': 0, 
'SW3dpid': 0 }
 
def _handle_ConnectionUp (event):
  # We remember the switch identifiers (DPID) for SW2 and SW3
  global lab4tools
  for m in event.connection.features.ports:
      if m.name == "SW2-eth1": 
          if lab4tools['FlagSW2']:
            lab4tools['SW2dpid'] = event.connection.dpid
            send_message_sw(event, lab4tools['IP2'], lab4tools['IP3'], lab4tools['SW2dpid'], 3)
            send_message_sw(event, lab4tools['IP3'], lab4tools['IP2'], lab4tools['SW2dpid'], 1)
            lab4tools['FlagSW2'] = False
          continue
      elif m.name == "SW3-eth1": 
          if lab4tools['FlagSW3']:
            lab4tools['SW3dpid'] = event.connection.dpid
            send_message_sw(event, lab4tools['IP2'], lab4tools['IP3'], lab4tools['SW3dpid'], 1)
            send_message_sw(event, lab4tools['IP3'], lab4tools['IP2'], lab4tools['SW3dpid'], 3)
            lab4tools['FlagSW3'] = False
          continue

def send_message_sw (event, srcip, dstip, switch, Pout):
  msg = of.ofp_flow_mod()
  msg.match.dl_type = 0x800
  msg.match.dpid = switch
  msg.priority = 1
  msg.match.nw_src = srcip
  msg.match.nw_dst = dstip
  msg.actions.append(of.ofp_action_output(port = Pout))
  log.info("Updating the table for switch %s" % dpid_to_str(switch))
  event.connection.send(msg)

def _handle_ConnectionDown (event):
  # We clear the flags and DPID's
  global lab4tools
  if event.connection.dpid == lab4tools['SW2dpid']:
      lab4tools['FlagSW2'] = True
      event.connection.send(of.ofp_flow_mod(command=of.OFPFC_DELETE))
      log.info('Forgetting switch: %s' % dpid_to_str(lab4tools['SW2dpid']))

  elif event.connection.dpid == lab4tools['SW3dpid']:
      lab4tools['FlagSW3'] = True
      event.connection.send(of.ofp_flow_mod(command=of.OFPFC_DELETE))
      log.info('Forgetting switch: %s' % dpid_to_str(lab4tools['SW3dpid']))

def launch ():
  def start_bypass ():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("ConnectionDown", _handle_ConnectionDown)
    log.info("Bypass component enabled")
  core.call_when_ready(start_bypass, "openflow_discovery")


