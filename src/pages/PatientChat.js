import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useSocket } from '../contexts/SocketContext';
import { Send, ArrowLeft, MessageCircle, Clock } from 'lucide-react';

const PatientChat = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { socket, isConnected, emitEvent } = useSocket();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [patientName, setPatientName] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (location.state) {
      setSessionId(location.state.sessionId);
      setPatientName(location.state.patientName);
    } else {
      // Redirect if no session data
      navigate('/');
    }
  }, [location.state, navigate]);

  useEffect(() => {
    if (!socket || !isConnected) return;

    // Join patient room
    socket.emit('join', { room: `patient_${sessionId}` });

    // Listen for bot responses
    socket.on('bot_response', (data) => {
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: data.message,
        isBot: true,
        timestamp: new Date(),
        type: data.type || 'chat'
      }]);
      setIsTyping(false);
    });

    // Listen for connection status
    socket.on('connect', () => {
      console.log('Connected to chat server');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from chat server');
    });

    return () => {
      socket.off('bot_response');
      socket.off('connect');
      socket.off('disconnect');
    };
  }, [socket, isConnected, sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || !isConnected) return;

    const newMessage = {
      id: Date.now(),
      text: inputMessage,
      isBot: false,
      timestamp: new Date(),
      type: 'chat'
    };

    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Send message to server
    emitEvent('patient_message', {
      session_id: sessionId,
      message: inputMessage
    });
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (!sessionId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <button
              onClick={() => navigate('/')}
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="h-5 w-5" />
              <span>Back to Home</span>
            </button>
            
            <div className="flex items-center space-x-3">
              <div className="bg-primary-100 p-2 rounded-full">
                <MessageCircle className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">Medical Triage Chat</h1>
                <p className="text-sm text-gray-500">Patient: {patientName}</p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm text-gray-500">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="card h-[600px] flex flex-col">
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-8">
                <MessageCircle className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Welcome to your triage session</h3>
                <p className="text-gray-500">Please describe your symptoms and answer the questions to help us assess your condition.</p>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isBot ? 'justify-start' : 'justify-end'}`}
              >
                <div className={`chat-bubble ${message.isBot ? 'bot' : 'user'}`}>
                  <p className="text-sm">{message.text}</p>
                  <div className={`flex items-center space-x-1 mt-1 text-xs ${
                    message.isBot ? 'text-gray-500' : 'text-blue-100'
                  }`}>
                    <Clock className="h-3 w-3" />
                    <span>{formatTime(message.timestamp)}</span>
                  </div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex justify-start">
                <div className="chat-bubble bot">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="border-t border-gray-200 p-4">
            <form onSubmit={handleSubmit} className="flex space-x-3">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 input-field"
                disabled={!isConnected}
              />
              <button
                type="submit"
                disabled={!inputMessage.trim() || !isConnected}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="h-4 w-4" />
              </button>
            </form>
            
            {!isConnected && (
              <p className="text-sm text-red-500 mt-2 text-center">
                Connection lost. Please refresh the page.
              </p>
            )}
          </div>
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            Be as detailed as possible when describing your symptoms. This helps our AI provide a more accurate assessment.
          </p>
        </div>
      </main>
    </div>
  );
};

export default PatientChat;

