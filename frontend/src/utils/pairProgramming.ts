import { io, Socket } from 'socket.io-client'

export interface PairProgrammingSession {
  session_id: string
  code: string
  output: string
  host_username: string
  participants: Array<{
    user_id?: number
    username: string
    socket_id: string
    joined_at: string
  }>
}

export interface ChatMessage {
  id: string
  username: string
  message: string
  timestamp: Date
}

export interface PairProgrammingCallbacks {
  onCodeUpdate?: (code: string, from: string) => void
  onOutputUpdate?: (output: string) => void
  onParticipantJoined?: (username: string, participants: any[]) => void
  onParticipantLeft?: (participants: any[]) => void
  onCursorUpdate?: (position: any, username: string, socketId: string) => void
  onSelectionUpdate?: (selection: any, username: string, socketId: string) => void
  onTypingStart?: (username: string) => void
  onTypingStop?: (username: string) => void
  onChatMessage?: (message: ChatMessage) => void
  onError?: (message: string) => void
}

class PairProgrammingClient {
  private socket: Socket | null = null
  private sessionId: string | null = null
  private callbacks: PairProgrammingCallbacks = {}
  private username: string = 'Anonymous'
  private userId: number | null = null

  connect() {
    if (this.socket?.connected) {
      return
    }

    this.socket = io('http://localhost:5000', {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 10,
      reconnectionDelayMax: 5000,
      timeout: 20000
    })

    this.socket.on('connect', () => {
      console.log('Connected to pair programming server')
      // Rejoin session if we have one
      if (this.sessionId) {
        this.joinSession(this.sessionId).catch(err => {
          console.error('Failed to rejoin session after reconnect:', err)
          if (this.callbacks.onError) {
            this.callbacks.onError('Failed to reconnect to session. Please refresh the page.')
          }
        })
      }
    })

    this.socket.on('disconnect', (reason: string) => {
      console.log('Disconnected from pair programming server:', reason)
      if (reason === 'io server disconnect') {
        // Server disconnected, try to reconnect
        this.socket?.connect()
      }
    })

    this.socket.on('connect_error', (error: Error) => {
      console.error('Connection error:', error)
      if (this.callbacks.onError) {
        this.callbacks.onError(`Connection error: ${error.message}`)
      }
    })

    this.socket.on('reconnect', (attemptNumber: number) => {
      console.log('Reconnected after', attemptNumber, 'attempts')
    })

    this.socket.on('reconnect_attempt', (attemptNumber: number) => {
      console.log('Reconnection attempt', attemptNumber)
    })

    this.socket.on('reconnect_error', (error: Error) => {
      console.error('Reconnection error:', error)
    })

    this.socket.on('reconnect_failed', () => {
      console.error('Failed to reconnect after all attempts')
      if (this.callbacks.onError) {
        this.callbacks.onError('Failed to reconnect to server. Please refresh the page.')
      }
    })

    this.socket.on('session_state', (data: any) => {
      if (this.callbacks.onCodeUpdate) {
        this.callbacks.onCodeUpdate(data.code, '')
      }
      if (this.callbacks.onOutputUpdate) {
        this.callbacks.onOutputUpdate(data.output)
      }
      // Load chat messages from session state
      if (data.messages && Array.isArray(data.messages) && this.callbacks.onChatMessage) {
        data.messages.forEach((msg: any) => {
          this.callbacks.onChatMessage!({
            id: Date.now().toString() + Math.random(),
            username: msg.username,
            message: msg.message,
            timestamp: new Date(msg.timestamp)
          })
        })
      }
    })

    this.socket.on('code_updated', (data: any) => {
      if (this.callbacks.onCodeUpdate) {
        this.callbacks.onCodeUpdate(data.code, data.from)
      }
    })

    this.socket.on('output_updated', (data: any) => {
      if (this.callbacks.onOutputUpdate) {
        this.callbacks.onOutputUpdate(data.output)
      }
    })

    this.socket.on('participant_joined', (data: any) => {
      if (this.callbacks.onParticipantJoined) {
        this.callbacks.onParticipantJoined(data.username, data.participants)
      }
    })

    this.socket.on('participant_left', (data: any) => {
      if (this.callbacks.onParticipantLeft) {
        this.callbacks.onParticipantLeft(data.participants)
      }
    })

    this.socket.on('cursor_updated', (data: any) => {
      if (this.callbacks.onCursorUpdate) {
        this.callbacks.onCursorUpdate(data.position, data.username, data.socket_id)
      }
    })

    this.socket.on('selection_updated', (data: any) => {
      if (this.callbacks.onSelectionUpdate) {
        this.callbacks.onSelectionUpdate(data.selection, data.username, data.socket_id)
      }
    })

    this.socket.on('typing_start', (data: any) => {
      if (this.callbacks.onTypingStart) {
        this.callbacks.onTypingStart(data.username)
      }
    })

    this.socket.on('typing_stop', (data: any) => {
      if (this.callbacks.onTypingStop) {
        this.callbacks.onTypingStop(data.username)
      }
    })

    this.socket.on('chat_message', (data: any) => {
      if (this.callbacks.onChatMessage) {
        this.callbacks.onChatMessage({
          id: data.id || Date.now().toString(),
          username: data.username,
          message: data.message,
          timestamp: new Date(data.timestamp || Date.now())
        })
      }
    })

    this.socket.on('error', (data: any) => {
      if (this.callbacks.onError) {
        this.callbacks.onError(data.message)
      }
    })
  }

  setCallbacks(callbacks: PairProgrammingCallbacks) {
    this.callbacks = callbacks
  }

  setUserInfo(username: string, userId: number | null = null) {
    this.username = username
    this.userId = userId
  }

  async createSession(): Promise<string> {
    try {
      const response = await fetch('http://localhost:5000/api/pair-programming/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: this.userId,
          username: this.username
        })
      })

      const data = await response.json()
      if (data.success) {
        this.sessionId = data.session_id
        return data.session_id
      } else {
        throw new Error(data.error || 'Failed to create session')
      }
    } catch (error: any) {
      throw new Error(`Failed to create session: ${error.message}`)
    }
  }

  async joinSession(sessionId: string): Promise<void> {
    if (!this.socket?.connected) {
      this.connect()
      // Wait for connection with timeout
      await new Promise<void>((resolve, reject) => {
        if (!this.socket) {
          reject(new Error('Socket not initialized'))
          return
        }
        
        if (this.socket.connected) {
          resolve()
          return
        }
        
        const timeout = setTimeout(() => {
          reject(new Error('Connection timeout'))
        }, 10000) // 10 second timeout
        
        this.socket.once('connect', () => {
          clearTimeout(timeout)
          resolve()
        })
        
        this.socket.once('connect_error', (error: Error) => {
          clearTimeout(timeout)
          reject(error)
        })
      })
    }

    this.sessionId = sessionId
    this.socket?.emit('join_session', {
      session_id: sessionId,
      user_id: this.userId,
      username: this.username
    })
  }

  leaveSession() {
    if (this.socket && this.sessionId) {
      this.socket.emit('leave_session', {
        session_id: this.sessionId
      })
      this.sessionId = null
    }
  }

  sendCodeChange(code: string) {
    if (this.socket && this.sessionId) {
      this.socket.emit('code_change', {
        session_id: this.sessionId,
        code: code,
        username: this.username
      })
    }
  }

  sendOutputChange(output: string) {
    if (this.socket && this.sessionId) {
      this.socket.emit('output_change', {
        session_id: this.sessionId,
        output: output
      })
    }
  }

  sendCursorChange(position: any) {
    if (this.socket && this.sessionId) {
      this.socket.emit('cursor_change', {
        session_id: this.sessionId,
        position: position,
        username: this.username
      })
    }
  }

  sendSelectionChange(selection: any) {
    if (this.socket && this.sessionId) {
      this.socket.emit('selection_change', {
        session_id: this.sessionId,
        selection: selection,
        username: this.username
      })
    }
  }

  sendChatMessage(message: string) {
    if (this.socket && this.sessionId && message.trim()) {
      this.socket.emit('chat_message', {
        session_id: this.sessionId,
        username: this.username,
        message: message.trim()
      })
    }
  }

  sendTypingStart() {
    if (this.socket && this.sessionId) {
      this.socket.emit('typing_start', {
        session_id: this.sessionId,
        username: this.username
      })
    }
  }

  sendTypingStop() {
    if (this.socket && this.sessionId) {
      this.socket.emit('typing_stop', {
        session_id: this.sessionId,
        username: this.username
      })
    }
  }

  async extendSession(hours: number = 24): Promise<boolean> {
    if (!this.sessionId) return false
    
    try {
      const response = await fetch(`http://localhost:5000/api/pair-programming/${this.sessionId}/extend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ hours })
      })
      
      const data = await response.json()
      return data.success || false
    } catch (error) {
      console.error('Failed to extend session:', error)
      return false
    }
  }

  async restoreSession(sessionId: string): Promise<boolean> {
    try {
      const response = await fetch(`http://localhost:5000/api/pair-programming/${sessionId}`)
      const data = await response.json()
      
      if (data.success && data.session) {
        this.sessionId = sessionId
        return true
      }
      return false
    } catch (error) {
      console.error('Failed to restore session:', error)
      return false
    }
  }

  saveSessionToStorage() {
    if (this.sessionId) {
      localStorage.setItem('pair_programming_session_id', this.sessionId)
    }
  }

  loadSessionFromStorage(): string | null {
    return localStorage.getItem('pair_programming_session_id')
  }

  clearSessionStorage() {
    localStorage.removeItem('pair_programming_session_id')
  }

  getSessionId(): string | null {
    return this.sessionId
  }

  isConnected(): boolean {
    return this.socket?.connected || false
  }

  disconnect() {
    this.leaveSession()
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }
}

export const pairProgrammingClient = new PairProgrammingClient()






