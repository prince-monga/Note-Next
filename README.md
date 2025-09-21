# NoteNext - Family Note Management System

A fullstack note-taking application with parent-child role management built with FastAPI and React.

## 🚀 Features

- **Role-Based Access**: Parents (read-only) and Children (full CRUD)
- **Parent-Child Linking**: Parents can select children during signup
- **Note Organization**: Folders, tags, and to-do functionality
- **Real-time Filtering**: Parents can view specific child's notes
- **Responsive Design**: Clean, modern interface

## 🛠 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite, JWT Authentication
- **Frontend**: React.js, TypeScript, Axios
- **Database**: SQLite (PostgreSQL for production)
- **Deployment**: Vercel

## 📦 Installation

### Local Development

1. **Clone Repository**
```bash
git clone <repository-url>
cd NoteNext
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python create_demo_data.py  # Create demo data
python main.py  # Start server on port 9002
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm start  # Start on port 3000
```

## 🌐 Deployment

### Vercel Deployment

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Deploy on Vercel**
- Connect GitHub repository to Vercel
- Vercel will automatically detect and deploy
- Backend runs on `/api` routes
- Frontend serves from root

### Environment Variables

For production, set these in Vercel dashboard:
```
DATABASE_URL=<postgresql-connection-string>
SECRET_KEY=<your-secret-key>
```

## 👥 Demo Users

**Parents:**
- `sunita` / `password123` (children: ananya, ishaan)
- `vikram` / `password123` (children: diya, aarav)

**Children:**
- `ananya` / `password123`
- `ishaan` / `password123`
- `diya` / `password123`
- `aarav` / `password123`

## 🎯 Usage Flow

1. **Signup**: Create parent account and select children
2. **Login**: Access role-based dashboard
3. **Parent View**: Select child to view their notes
4. **Child View**: Full CRUD access to own notes

## 📁 Project Structure

```
NoteNext/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── vercel_main.py       # Vercel-compatible version
│   ├── database.py          # SQLAlchemy models
│   ├── auth.py              # JWT authentication
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── api.ts          # API service layer
│   │   ├── types.ts        # TypeScript interfaces
│   │   └── App.tsx         # Main application
│   └── package.json        # Node dependencies
├── vercel.json             # Vercel configuration
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /api/signup` - Create user with child selection
- `POST /api/login` - Login with JWT token
- `GET /api/available-children` - Get unlinked children

### Data Management
- `GET /api/children` - Get parent's children
- `GET /api/folders` - Get folders (filtered by role)
- `GET /api/notes` - Get notes (filtered by child/folder)
- `POST /api/notes` - Create note (children only)
- `PUT /api/notes/{id}` - Update note (children only)
- `DELETE /api/notes/{id}` - Delete note (children only)

## 🎨 Key Features Explained

### Parent-Child Relationship
- Parents signup and select existing children
- Children are created independently first
- Parents see only their linked children's data

### Role-Based Access Control
- **Parents**: Read-only access, can view all children's content
- **Children**: Full CRUD access to their own content only

### Child Filtering
- Parents can select specific child from sidebar
- All folders and notes filter by selected child
- Clean UI state management

## 🚀 Production Considerations

- Replace SQLite with PostgreSQL for production
- Add proper error handling and logging
- Implement rate limiting
- Add data validation and sanitization
- Set up proper environment variable management

## 📄 License

MIT License - Feel free to use for educational purposes.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

**Built for interview demonstration - showcases fullstack development, role-based access control, and modern deployment practices.**