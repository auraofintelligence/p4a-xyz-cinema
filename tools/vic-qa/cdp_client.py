"""Small dependency-free Chrome DevTools client for isolated headless QA."""
import socket, json, struct, os, base64, urllib.request, urllib.parse, time
class CDP:
 def __init__(self,port=9227):
  opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
  tabs=json.load(opener.open(f'http://127.0.0.1:{port}/json'))
  u=urllib.parse.urlsplit(next(t['webSocketDebuggerUrl'] for t in tabs if t['type']=='page'))
  self.s=socket.create_connection((u.hostname,u.port),timeout=60);self.seq=0;self.events=[]
  key=base64.b64encode(os.urandom(16)).decode()
  self.s.sendall(f'GET {u.path} HTTP/1.1\r\nHost: {u.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode())
  response=b''
  while b'\r\n\r\n' not in response:response+=self.s.recv(1)
  assert response.startswith(b'HTTP/1.1 101 '),response
 def exact(self,n):
  out=b''
  while len(out)<n:
   chunk=self.s.recv(n-len(out))
   if not chunk:raise EOFError()
   out+=chunk
  return out
 def send(self,payload):
  data=json.dumps(payload).encode();mask=os.urandom(4);n=len(data)
  header=bytes([129,128|n]) if n<126 else bytes([129,254])+struct.pack('!H',n) if n<65536 else bytes([129,255])+struct.pack('!Q',n)
  self.s.sendall(header+mask+bytes(v^mask[i%4] for i,v in enumerate(data)))
 def recv(self):
  data=b''
  while True:
   first,second=self.exact(2);n=second&127
   if n==126:n=struct.unpack('!H',self.exact(2))[0]
   elif n==127:n=struct.unpack('!Q',self.exact(8))[0]
   mask=self.exact(4) if second&128 else None
   chunk=self.exact(n)
   if mask:chunk=bytes(v^mask[i%4] for i,v in enumerate(chunk))
   data+=chunk
   if first&128:return json.loads(data)
 def call(self,method,params=None):
  self.seq+=1;ident=self.seq;self.send({'id':ident,'method':method,'params':params or {}})
  while True:
   r=self.recv()
   if r.get('id')==ident:
    if 'error'in r:raise RuntimeError(r['error'])
    return r.get('result',{})
   self.events.append(r)
 def evaluate(self,expression):
  r=self.call('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':True})
  if 'exceptionDetails'in r:raise RuntimeError(r['exceptionDetails'])
  return r.get('result',{}).get('value')
 def wait(self,expression,seconds=45):
  deadline=time.time()+seconds
  while time.time()<deadline:
   result=self.evaluate(expression)
   if result:return result
   time.sleep(.25)
  raise TimeoutError(expression)
