import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, 
  Upload, 
  FileText, 
  Database, 
  Cpu, 
  Plus, 
  MessageSquare, 
  PieChart, 
  Layers,
  ChevronRight,
  Loader2,
  Trash2
} from 'lucide-react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE_URL = "http://localhost:8000";

const App = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hello! I'm DataPilot. Upload your CSV or PDF files, and I'll help you analyze them. What's on your mind today?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_BASE_URL}/upload`, formData);
      setFiles(prev => [...prev, { name: file.name, type: file.name.endsWith('.csv') ? 'CSV' : 'PDF' }]);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `Successfully uploaded ${file.name}. ${res.data.message}` 
      }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'assistant', content: `Failed to upload ${file.name}. Is the backend running?` }]);
    } finally {
      setUploading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('message', userMessage);
      const res = await axios.post(`${API_BASE_URL}/chat`, formData);
      
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response || res.data.error }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error. Please check if the backend is running and your OpenAI API key is valid." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {/* Sidebar */}
      <div className="w-80 border-r border-white/10 flex flex-col bg-secondary/30 backdrop-blur-xl">
        <div className="p-6 border-b border-white/10 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center shadow-lg shadow-primary/20">
            <Cpu className="text-white" size={24} />
          </div>
          <div>
            <h1 className="font-bold text-xl tracking-tight">DataPilot</h1>
            <p className="text-xs text-white/40">Hybrid RAG Agent</p>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          <div>
            <h3 className="text-xs font-semibold text-white/30 uppercase tracking-wider mb-3 px-2">Data Sources</h3>
            <div className="space-y-2">
              <label className="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 cursor-pointer transition-all">
                <Plus size={18} className="text-primary" />
                <span className="text-sm font-medium">Upload File</span>
                <input type="file" className="hidden" onChange={handleFileUpload} accept=".csv,.pdf" />
                {uploading && <Loader2 size={16} className="animate-spin ml-auto" />}
              </label>
              
              <div className="mt-4 space-y-2">
                {files.map((file, idx) => (
                  <div key={idx} className="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/10 group">
                    {file.type === 'CSV' ? <Database size={16} className="text-blue-400" /> : <FileText size={16} className="text-red-400" />}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">{file.name}</p>
                      <p className="text-[10px] text-white/40">{file.type}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-semibold text-white/30 uppercase tracking-wider mb-3 px-2">Capabilities</h3>
            <div className="space-y-1">
              <div className="flex items-center gap-3 p-2 text-sm text-white/60">
                <Layers size={16} />
                <span>SQL Engine</span>
              </div>
              <div className="flex items-center gap-3 p-2 text-sm text-white/60">
                <PieChart size={16} />
                <span>Vector RAG</span>
              </div>
              <div className="flex items-center gap-3 p-2 text-sm text-white/60">
                <MessageSquare size={16} />
                <span>LLM Reasoning</span>
              </div>
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-white/10">
          <div className="p-4 rounded-2xl bg-gradient-to-br from-primary/20 to-transparent border border-primary/20">
            <p className="text-xs font-medium text-primary-light">Pro Tip</p>
            <p className="text-[11px] text-white/60 mt-1">Ask "Why did sales drop?" for RAG-based insights.</p>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative">
        {/* Header */}
        <div className="h-16 border-b border-white/10 flex items-center justify-between px-8 bg-background/50 backdrop-blur-md sticky top-0 z-10">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            <span className="text-sm font-medium text-white/60">Agent Status: Ready</span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8">
          <AnimatePresence initial={false}>
            {messages.map((msg, idx) => (
              <motion.div 
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[80%] flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                  <div className={`w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center ${
                    msg.role === 'user' ? 'bg-secondary border border-white/10' : 'bg-primary'
                  }`}>
                    {msg.role === 'user' ? '👤' : <Cpu size={20} className="text-white" />}
                  </div>
                  <div className={`p-5 rounded-3xl ${
                    msg.role === 'user' 
                      ? 'bg-primary text-white rounded-tr-none' 
                      : 'bg-white/5 border border-white/10 rounded-tl-none'
                  }`}>
                    <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
                  <Cpu size={20} className="text-white" />
                </div>
                <div className="p-5 rounded-3xl bg-white/5 border border-white/10 rounded-tl-none flex items-center gap-3">
                  <Loader2 size={18} className="animate-spin text-primary" />
                  <span className="text-sm text-white/60 tracking-tight">Thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-8 pt-0">
          <div className="max-w-4xl mx-auto relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-primary to-blue-600 rounded-3xl blur opacity-20 group-focus-within:opacity-40 transition duration-1000"></div>
            <div className="relative flex items-center bg-secondary border border-white/10 rounded-2xl p-2 pr-4 shadow-2xl">
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask DataPilot anything about your data..."
                className="flex-1 bg-transparent border-none focus:ring-0 text-white placeholder-white/20 px-4 py-3"
              />
              <button 
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                className={`p-3 rounded-xl transition-all ${
                  input.trim() && !isLoading 
                    ? 'bg-primary text-white shadow-lg shadow-primary/20 hover:scale-105 active:scale-95' 
                    : 'text-white/20'
                }`}
              >
                <Send size={20} />
              </button>
            </div>
          </div>
          <p className="text-center text-[10px] text-white/20 mt-4 tracking-widest uppercase font-medium">Powered by Hybrid RAG Engine</p>
        </div>
      </div>
    </div>
  );
};

export default App;
