import React, { useState, useEffect } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, onAuthStateChanged, signInAnonymously, signInWithCustomToken } from 'firebase/auth';
import { getFirestore, collection, onSnapshot, query, doc, setDoc } from 'firebase/firestore';
import { 
  MessageSquare, 
  Send, 
  Users, 
  Settings, 
  Search, 
  Phone, 
  MoreVertical,
  CheckCheck,
  Clock,
  AlertCircle
} from 'lucide-react';

// Initialize Firebase using environment globals
const firebaseConfig = JSON.parse(__firebase_config);
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const appId = typeof __app_id !== 'undefined' ? __app_id : 'sms-backend-app';

export default function App() {
  const [user, setUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [selectedContact, setSelectedContact] = useState(null);
  const [newMessage, setNewMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  // Auth Logic
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
          await signInWithCustomToken(auth, __initial_auth_token);
        } else {
          await signInAnonymously(auth);
        }
      } catch (error) {
        console.error("Auth failed:", error);
      }
    };
    initAuth();
    const unsubscribe = onAuthStateChanged(auth, setUser);
    return () => unsubscribe();
  }, []);

  // Real-time Data Fetching
  useEffect(() => {
    if (!user) return;

    // Listen to messages collection
    // Note: We use a simple collection query per Rule 2 (No complex queries)
    const messagesRef = collection(db, 'artifacts', appId, 'public', 'data', 'messages');
    
    const unsubscribe = onSnapshot(messagesRef, (snapshot) => {
      const msgs = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      
      // Sort in memory instead of Firestore to avoid index requirements
      const sortedMsgs = msgs.sort((a, b) => b.timestamp - a.timestamp);
      setMessages(sortedMsgs);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error:", error);
      setLoading(false);
    });

    return () => unsubscribe();
  }, [user]);

  // UI Derived State
  const contacts = Array.from(new Set(messages.map(m => m.sender))).map(phone => {
    const lastMsg = messages.find(m => m.sender === phone || m.receiver === phone);
    return {
      phone,
      lastMessage: lastMsg?.text || '',
      timestamp: lastMsg?.timestamp || 0
    };
  }).sort((a, b) => b.timestamp - a.timestamp);

  const filteredContacts = contacts.filter(c => 
    c.phone.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const activeMessages = messages
    .filter(m => m.sender === selectedContact || m.receiver === selectedContact)
    .sort((a, b) => a.timestamp - b.timestamp);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedContact || !user) return;

    const messageData = {
      text: newMessage,
      sender: 'system', // or a specific system number
      receiver: selectedContact,
      timestamp: Date.now(),
      status: 'pending',
      userId: user.uid
    };

    try {
      const msgId = crypto.randomUUID();
      const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'messages', msgId);
      await setDoc(docRef, messageData);
      setNewMessage('');
    } catch (err) {
      console.error("Send error:", err);
    }
  };

  if (!user) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-slate-100 text-slate-900 font-sans">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-4 border-b border-slate-200 flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600 flex items-center gap-2">
            <MessageSquare size={24} />
            Inbox
          </h1>
          <button className="p-2 hover:bg-slate-100 rounded-full transition-colors">
            <Settings size={20} className="text-slate-500" />
          </button>
        </div>

        <div className="p-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input 
              type="text"
              placeholder="Search contacts..."
              className="w-full pl-10 pr-4 py-2 bg-slate-100 border-none rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto">
          {filteredContacts.map((contact) => (
            <div 
              key={contact.phone}
              onClick={() => setSelectedContact(contact.phone)}
              className={`p-4 cursor-pointer hover:bg-slate-50 border-b border-slate-100 transition-colors ${selectedContact === contact.phone ? 'bg-blue-50 border-l-4 border-l-blue-600' : ''}`}
            >
              <div className="flex justify-between items-start mb-1">
                <span className="font-semibold text-slate-800">{contact.phone}</span>
                <span className="text-xs text-slate-400">
                  {new Date(contact.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <p className="text-sm text-slate-500 truncate">{contact.lastMessage}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-white">
        {selectedContact ? (
          <>
            {/* Chat Header */}
            <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-white shadow-sm z-10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                  <Phone size={20} />
                </div>
                <div>
                  <h2 className="font-bold text-slate-800">{selectedContact}</h2>
                  <span className="text-xs text-green-500 flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-green-500"></span>
                    Online
                  </span>
                </div>
              </div>
              <div className="flex gap-2">
                <button className="p-2 hover:bg-slate-100 rounded-full"><Search size={20} className="text-slate-500" /></button>
                <button className="p-2 hover:bg-slate-100 rounded-full"><MoreVertical size={20} className="text-slate-500" /></button>
              </div>
            </div>

            {/* Messages List */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-[#f8fafc]">
              {activeMessages.map((msg) => (
                <div 
                  key={msg.id} 
                  className={`flex ${msg.sender === 'system' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[70%] p-3 rounded-2xl shadow-sm relative group ${
                    msg.sender === 'system' 
                      ? 'bg-blue-600 text-white rounded-tr-none' 
                      : 'bg-white text-slate-800 border border-slate-100 rounded-tl-none'
                  }`}>
                    <p className="text-sm leading-relaxed">{msg.text}</p>
                    <div className={`flex items-center gap-1 mt-1 justify-end ${msg.sender === 'system' ? 'text-blue-100' : 'text-slate-400'}`}>
                      <span className="text-[10px]">
                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                      {msg.sender === 'system' && <CheckCheck size={12} />}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Input Area */}
            <form onSubmit={handleSendMessage} className="p-4 border-t border-slate-200 bg-white">
              <div className="flex items-center gap-3 bg-slate-100 rounded-2xl p-2 pr-3">
                <input 
                  type="text"
                  placeholder="Type your message..."
                  className="flex-1 bg-transparent border-none focus:ring-0 px-3 py-2 outline-none text-slate-800"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                />
                <button 
                  type="submit"
                  disabled={!newMessage.trim()}
                  className="bg-blue-600 text-white p-2 rounded-xl hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send size={20} />
                </button>
              </div>
            </form>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-400 bg-slate-50">
            <div className="w-20 h-20 bg-white rounded-3xl shadow-lg flex items-center justify-center mb-4">
              <MessageSquare size={40} className="text-blue-500" />
            </div>
            <h3 className="text-xl font-semibold text-slate-700">Select a conversation</h3>
            <p className="text-sm">Choose a contact from the list to start messaging</p>
          </div>
        )}
      </div>
    </div>
  );
}
