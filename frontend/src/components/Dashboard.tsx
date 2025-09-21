import React, { useState, useEffect } from 'react';
import { User, Folder, Note, Child } from '../types';
import { foldersAPI, notesAPI, childrenAPI } from '../api';

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ user, onLogout }) => {
  const [folders, setFolders] = useState<Folder[]>([]);
  const [notes, setNotes] = useState<Note[]>([]);
  const [children, setChildren] = useState<Child[]>([]);
  const [selectedChild, setSelectedChild] = useState<Child | null>(null);
  const [selectedFolder, setSelectedFolder] = useState<number | null>(null);
  const [showNoteForm, setShowNoteForm] = useState(false);

  const [editingNote, setEditingNote] = useState<Note | null>(null);

  const [noteForm, setNoteForm] = useState({
    title: '',
    content: '',
    tags: '',
    is_todo: false,
    folder_id: undefined as number | undefined
  });



  useEffect(() => {
    const initializeData = async () => {
      if (user.role === 'parent') {
        try {
          const response = await childrenAPI.getAll();
          setChildren(response.data);
          if (response.data.length > 0) {
            const firstChild = response.data[0];
            setSelectedChild(firstChild);
            const foldersResponse = await foldersAPI.getAll(firstChild.id);
            setFolders(foldersResponse.data);
            const notesResponse = await notesAPI.getAll(undefined, firstChild.id);
            setNotes(notesResponse.data);
          }
        } catch (error) {
          console.error('Error loading parent data:', error);
        }
      } else {
        try {
          const [foldersResponse, notesResponse] = await Promise.all([
            foldersAPI.getAll(),
            notesAPI.getAll()
          ]);
          setFolders(foldersResponse.data);
          setNotes(notesResponse.data);
        } catch (error) {
          console.error('Error loading child data:', error);
        }
      }
    };
    
    initializeData();
  }, [user.role]);



  const loadFolders = async (childId?: number) => {
    try {
      const response = await foldersAPI.getAll(childId);
      setFolders(response.data);
    } catch (error) {
      console.error('Error loading folders:', error);
    }
  };

  const loadNotes = async (folderId?: number, childId?: number) => {
    try {
      const response = await notesAPI.getAll(folderId, childId);
      setNotes(response.data);
    } catch (error) {
      console.error('Error loading notes:', error);
    }
  };



  const handleCreateNote = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingNote) {
        await notesAPI.update(editingNote.id, noteForm);
        setEditingNote(null);
      } else {
        await notesAPI.create(noteForm);
      }
      setNoteForm({ title: '', content: '', tags: '', is_todo: false, folder_id: undefined });
      setShowNoteForm(false);
      const childId = user.role === 'parent' ? selectedChild?.id : undefined;
      loadNotes(selectedFolder || undefined, childId);
    } catch (error) {
      console.error('Error saving note:', error);
    }
  };

  const handleDeleteNote = async (noteId: number) => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      try {
        await notesAPI.delete(noteId);
        const childId = user.role === 'parent' ? selectedChild?.id : undefined;
        loadNotes(selectedFolder || undefined, childId);
      } catch (error) {
        console.error('Error deleting note:', error);
      }
    }
  };

  const handleToggleTodo = async (note: Note) => {
    try {
      await notesAPI.update(note.id, { is_completed: !note.is_completed });
      const childId = user.role === 'parent' ? selectedChild?.id : undefined;
      loadNotes(selectedFolder || undefined, childId);
    } catch (error) {
      console.error('Error updating note:', error);
    }
  };

  const startEditNote = (note: Note) => {
    setEditingNote(note);
    setNoteForm({
      title: note.title,
      content: note.content,
      tags: note.tags,
      is_todo: note.is_todo,
      folder_id: note.folder_id
    });
    setShowNoteForm(true);
  };



  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>NoteNext</h1>
        <div className="user-info">
          <span>Welcome, {user.username} ({user.role})</span>
          <button onClick={onLogout}>Logout</button>
        </div>
      </header>

      <div className="dashboard-content">
        <aside className="sidebar">
          {user.role === 'parent' && (
            <div className="children-section">
              <div className="section-header">
                <h3>Children</h3>
              </div>
              <div className="children-list">
                {children.map(child => (
                  <button
                    key={child.id}
                    className={selectedChild?.id === child.id ? 'active' : ''}
                    onClick={() => {
                      setSelectedChild(child);
                      setSelectedFolder(null);
                      loadFolders(child.id);
                      loadNotes(undefined, child.id);
                    }}
                  >
                    {child.username}
                  </button>
                ))}
              </div>
            </div>
          )}
          
          <div className="folders-section">
            <div className="section-header">
              <h3>📝 Notes</h3>
            </div>
            <div className="folder-list">
              <button
                className={selectedFolder === null ? 'active all-notes-btn' : 'all-notes-btn'}
                onClick={() => {
                  setSelectedFolder(null);
                  const childId = user.role === 'parent' ? selectedChild?.id : undefined;
                  loadNotes(undefined, childId);
                }}
              >
                📋 All Notes
              </button>
              {folders.map(folder => (
                <button
                  key={folder.id}
                  className={selectedFolder === folder.id ? 'active' : ''}
                  onClick={() => {
                    setSelectedFolder(folder.id);
                    const childId = user.role === 'parent' ? selectedChild?.id : undefined;
                    loadNotes(folder.id, childId);
                  }}
                >
                  📁 {folder.name}
                </button>
              ))}
            </div>
            {user.role === 'child' && (
              <div className="add-folder-section">
                <button 
                  className="add-folder-btn"
                  onClick={() => {
                    const folderName = prompt('Enter folder name:');
                    if (folderName) {
                      foldersAPI.create(folderName).then(() => {
                        loadFolders();
                      }).catch(error => {
                        console.error('Error creating folder:', error);
                      });
                    }
                  }}
                >
                  ➕ Add Folder
                </button>
              </div>
            )}
          </div>
        </aside>

        <main className="main-content">
          <div className="notes-header">
            <div className="notes-title">
              <h2>
                {selectedFolder ? (
                  <>
                    📁 {folders.find(f => f.id === selectedFolder)?.name}
                    <span className="note-count">({notes.length} notes)</span>
                  </>
                ) : (
                  <>
                    📋 All Notes
                    <span className="note-count">({notes.length} notes)</span>
                  </>
                )}
              </h2>
              {user.role === 'parent' && selectedChild && (
                <p className="viewing-child">Viewing notes from: <strong>{selectedChild.username}</strong></p>
              )}
            </div>
            {user.role === 'child' && (
              <button className="add-note-btn" onClick={() => setShowNoteForm(true)}>
                ➕ Add Note
              </button>
            )}
          </div>

          <div className="notes-grid">
            {notes.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📝</div>
                <h3>No notes found</h3>
                <p>
                  {selectedFolder 
                    ? `No notes in "${folders.find(f => f.id === selectedFolder)?.name}" folder yet.`
                    : user.role === 'parent' && selectedChild
                    ? `${selectedChild.username} hasn't created any notes yet.`
                    : 'No notes created yet.'
                  }
                </p>
                {user.role === 'child' && (
                  <button className="empty-action-btn" onClick={() => setShowNoteForm(true)}>
                    ➕ Create your first note
                  </button>
                )}
              </div>
            ) : (
              notes.map(note => (
                <div key={note.id} className={`note-card ${note.is_todo ? 'todo' : ''}`}>
                  <div className="note-header">
                    <h3>{note.title}</h3>
                    {user.role === 'child' && (
                      <div className="note-actions">
                        <button onClick={() => startEditNote(note)}>Edit</button>
                        <button onClick={() => handleDeleteNote(note.id)}>Delete</button>
                      </div>
                    )}
                  </div>
                  
                  {note.is_todo && (
                    <div className="todo-checkbox">
                      <input
                        type="checkbox"
                        checked={note.is_completed}
                        onChange={() => handleToggleTodo(note)}
                        disabled={user.role === 'parent'}
                      />
                      <span className={note.is_completed ? 'completed' : ''}>
                        {note.is_completed ? 'Completed' : 'Pending'}
                      </span>
                    </div>
                  )}
                  
                  <p className="note-content">{note.content}</p>
                  
                  {note.tags && (
                    <div className="note-tags">
                      {note.tags.split(',').map((tag, index) => (
                        <span key={index} className="tag">{tag.trim()}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </main>
      </div>



      {/* Note Form Modal */}
      {showNoteForm && (
        <div className="modal">
          <div className="modal-content">
            <h3>{editingNote ? 'Edit Note' : 'Create Note'}</h3>
            <form onSubmit={handleCreateNote}>
              <input
                type="text"
                placeholder="Note title"
                value={noteForm.title}
                onChange={(e) => setNoteForm({ ...noteForm, title: e.target.value })}
                required
              />
              
              <textarea
                placeholder="Note content"
                value={noteForm.content}
                onChange={(e) => setNoteForm({ ...noteForm, content: e.target.value })}
                rows={5}
                required
              />
              
              <input
                type="text"
                placeholder="Tags (comma-separated)"
                value={noteForm.tags}
                onChange={(e) => setNoteForm({ ...noteForm, tags: e.target.value })}
              />
              

              
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={noteForm.is_todo}
                  onChange={(e) => setNoteForm({ ...noteForm, is_todo: e.target.checked })}
                />
                This is a to-do item
              </label>
              
              <div className="modal-actions">
                <button type="submit">{editingNote ? 'Update' : 'Create'}</button>
                <button type="button" onClick={() => {
                  setShowNoteForm(false);
                  setEditingNote(null);
                  setNoteForm({ title: '', content: '', tags: '', is_todo: false, folder_id: undefined });
                }}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;