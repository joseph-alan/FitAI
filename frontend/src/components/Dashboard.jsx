import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import appIcon from '../assets/app-icon.png'
import logoutIcon from '../assets/clipart1764200.png'
import api from '../services/api'
import './Dashboard.css'

// Import muscle group icons
import abdominalsIcon from '../assets/muscle-icons/abdomnials.png'
import abductorsIcon from '../assets/muscle-icons/abductors.png'
import adductorsIcon from '../assets/muscle-icons/adductors.png'
import bicepsIcon from '../assets/muscle-icons/biceps.png'
import calvesIcon from '../assets/muscle-icons/calves.png'
import chestIcon from '../assets/muscle-icons/chest.png'
import forearmsIcon from '../assets/muscle-icons/forearms.png'
import glutesIcon from '../assets/muscle-icons/glutes.png'
import hamstringsIcon from '../assets/muscle-icons/hamstrings.png'
import latsIcon from '../assets/muscle-icons/lats.png'
import lowerBackIcon from '../assets/muscle-icons/lower back.png'
import middleBackIcon from '../assets/muscle-icons/middle back.png'
import neckIcon from '../assets/muscle-icons/neck.png'
import quadricepsIcon from '../assets/muscle-icons/quadriceps.png'
import shouldersIcon from '../assets/muscle-icons/shoulders.png'
import trapsIcon from '../assets/muscle-icons/traps.png'
import tricepsIcon from '../assets/muscle-icons/triceps.png'

function Dashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('dashboard')
  const [sidebarHovered, setSidebarHovered] = useState(false)
  const [muscleGroups, setMuscleGroups] = useState([])
  const [exercises, setExercises] = useState([])
  const [selectedMuscleGroup, setSelectedMuscleGroup] = useState('')
  const [selectedExercise, setSelectedExercise] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!user || !token) {
      navigate('/login')
    }
  }, [user, navigate])

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const handleSidebarMouseEnter = () => {
    setSidebarHovered(true)
  }

  const handleSidebarMouseLeave = () => {
    setSidebarHovered(false)
  }

  // Fetch muscle groups when workouts tab is selected
  useEffect(() => {
    if (activeTab === 'workouts') {
      fetchMuscleGroups()
    }
  }, [activeTab])

  const fetchMuscleGroups = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await api.get('/api/exercises/muscle-groups')
      setMuscleGroups(response.data.muscle_groups || [])
    } catch (err) {
      console.error('Error fetching muscle groups:', err)
      setError(`Failed to load muscle groups: ${err.response?.data?.message || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const fetchExercises = async (muscleGroup) => {
    setLoading(true)
    setError('')
    try {
      const response = await api.get(`/api/exercises/muscle-group/${muscleGroup}`)
      setExercises(response.data.exercises || [])
      setSelectedMuscleGroup(muscleGroup)
    } catch (err) {
      console.error('Error fetching exercises:', err)
      setError(`Failed to load exercises: ${err.response?.data?.message || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleMuscleGroupClick = (muscleGroup) => {
    fetchExercises(muscleGroup)
  }

  const handleExerciseClick = (exercise) => {
    setSelectedExercise(exercise)
  }

  const handleBackToMuscleGroups = () => {
    setExercises([])
    setSelectedMuscleGroup('')
    setSelectedExercise(null)
  }

  const handleBackToExercises = () => {
    setSelectedExercise(null)
  }

  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: '📊',
      description: 'Overview of your fitness journey'
    },
    {
      id: 'workouts',
      label: 'Workouts',
      icon: '💪',
      description: 'Track and manage your workouts'
    },
    {
      id: 'plan',
      label: 'Plan',
      icon: '📋',
      description: 'Create and manage your workout plans'
    },
    {
      id: 'progress',
      label: 'Progress',
      icon: '📈',
      description: 'View your fitness progress'
    },
    {
      id: 'goals',
      label: 'Goals',
      icon: '🎯',
      description: 'Set and track your fitness goals'
    },
    {
      id: 'profile',
      label: 'Profile',
      icon: '👤',
      description: 'Manage your account settings'
    }
  ]

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <div className="content-section">
            <h2>Welcome back, {user?.first_name || 'User'}! 👋</h2>
            <p className="subtitle">Here's your fitness overview for today</p>
            
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">🔥</div>
                <div className="stat-info">
                  <h3>7</h3>
                  <p>Workouts this week</p>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">⏱️</div>
                <div className="stat-info">
                  <h3>45 min</h3>
                  <p>Average session</p>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📈</div>
                <div className="stat-info">
                  <h3>85%</h3>
                  <p>Goal completion</p>
                </div>
              </div>
            </div>

            <div className="recent-activity">
              <h3>Recent Activity</h3>
              <div className="activity-list">
                <div className="activity-item">
                  <div className="activity-icon">🏋️</div>
                  <div className="activity-content">
                    <h4>Upper Body Workout</h4>
                    <p>Completed 45 minutes ago</p>
                  </div>
                </div>
                <div className="activity-item">
                  <div className="activity-icon">🏃</div>
                  <div className="activity-content">
                    <h4>Cardio Session</h4>
                    <p>Completed 2 hours ago</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      case 'workouts':
        return (
          <div className="content-section">
            {selectedExercise ? (
              // Exercise Detail View
              <div className="exercise-detail">
                <div className="exercise-detail-header">
                  <button 
                    onClick={handleBackToExercises}
                    className="back-button"
                  >
                    ← Back to Exercises
                  </button>
                  <h2>{selectedExercise.name}</h2>
                </div>
                
                <div className="exercise-images">
                  {selectedExercise.images && selectedExercise.images.length > 0 && (
                    selectedExercise.images.map((image, index) => (
                      <img 
                        key={index}
                        src={`https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/${image}`}
                        alt={`${selectedExercise.name} - Image ${index + 1}`}
                        className="exercise-image"
                      />
                    ))
                  )}
                </div>
                
                <div className="exercise-info">
                  <div className="exercise-section">
                    <h3>Equipment</h3>
                    <p>{selectedExercise.equipment}</p>
                  </div>
                  
                  <div className="exercise-section">
                    <h3>Primary Muscles</h3>
                    <div className="muscle-tags">
                      {selectedExercise.primary_muscles.map((muscle, index) => (
                        <span key={index} className="muscle-tag primary">{muscle}</span>
                      ))}
                    </div>
                  </div>
                  
                  {selectedExercise.secondary_muscles && selectedExercise.secondary_muscles.length > 0 && (
                    <div className="exercise-section">
                      <h3>Secondary Muscles</h3>
                      <div className="muscle-tags">
                        {selectedExercise.secondary_muscles.map((muscle, index) => (
                          <span key={index} className="muscle-tag secondary">{muscle}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div className="exercise-section">
                    <h3>Instructions</h3>
                    <div className="instructions">
                      {selectedExercise.instructions.split('\n').map((instruction, index) => (
                        <p key={index} className="instruction-step">{instruction}</p>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ) : exercises.length > 0 ? (
              // Exercises List View
              <div className="exercises-list">
                <div className="exercises-header">
                  <button 
                    onClick={handleBackToMuscleGroups}
                    className="back-button"
                  >
                    ← Back to Muscle Groups
                  </button>
                  <h2>Exercises for {formatMuscleGroupName(selectedMuscleGroup)}</h2>
                  <p className="subtitle">{exercises.length} exercises found</p>
                </div>
                
                {loading && (
                  <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading exercises...</p>
                  </div>
                )}
                
                {error && (
                  <div className="error-message">
                    {error}
                  </div>
                )}
                
                {!loading && !error && exercises.length > 0 && (
                  <div className="exercises-grid">
                    {exercises.map((exercise) => (
                      <div 
                        key={exercise.id} 
                        className="exercise-card"
                        onClick={() => handleExerciseClick(exercise)}
                      >
                        <div className="exercise-image-container">
                          {exercise.images && exercise.images.length > 0 && (
                            <img 
                              src={`https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/${exercise.images[0]}`}
                              alt={exercise.name}
                              className="exercise-thumbnail"
                            />
                          )}
                        </div>
                        <div className="exercise-card-content">
                          <h3 className="exercise-name">{exercise.name}</h3>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              // Muscle Groups View
              <div>
                <h2>Explore Workouts</h2>
                <p className="subtitle">Choose a muscle group to discover exercises</p>
                
                {loading && (
                  <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading muscle groups...</p>
                  </div>
                )}
                
                {error && (
                  <div className="error-message">
                    {error}
                  </div>
                )}
                
                {!loading && !error && muscleGroups.length > 0 && (
                  <div className="muscle-groups-grid">
                    {muscleGroups.map((muscleGroup, index) => (
                      <div 
                        key={index} 
                        className="muscle-group-card"
                        onClick={() => handleMuscleGroupClick(muscleGroup)}
                      >
                        <div className="muscle-group-icon">
                          {getMuscleGroupIcon(muscleGroup)}
                        </div>
                        <h3 className="muscle-group-name">
                          {formatMuscleGroupName(muscleGroup)}
                        </h3>
                        <p className="muscle-group-description">
                          Explore exercises for {formatMuscleGroupName(muscleGroup).toLowerCase()}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
                {!loading && !error && muscleGroups.length === 0 && (
                  <div className="error-message">
                    No muscle groups found. Please check your connection and try again.
                  </div>
                )}
              </div>
            )}
          </div>
        )
      case 'plan':
        return (
          <div className="content-section">
            <h2>Workout Planning</h2>
            <p className="subtitle">Create and manage your workout plans</p>
            <div className="placeholder-content">
              <div className="placeholder-card">
                <h3>Create Plan</h3>
                <p>Design custom workout routines</p>
              </div>
              <div className="placeholder-card">
                <h3>My Plans</h3>
                <p>View and manage your saved plans</p>
              </div>
            </div>
          </div>
        )
      case 'progress':
        return (
          <div className="content-section">
            <h2>Progress Tracking</h2>
            <p className="subtitle">Monitor your fitness journey</p>
            <div className="placeholder-content">
              <div className="placeholder-card">
                <h3>Weight Tracking</h3>
                <p>Track your weight and body composition</p>
              </div>
              <div className="placeholder-card">
                <h3>Strength Progress</h3>
                <p>Monitor your strength improvements</p>
              </div>
            </div>
          </div>
        )
      case 'goals':
        return (
          <div className="content-section">
            <h2>Fitness Goals</h2>
            <p className="subtitle">Set and achieve your fitness objectives</p>
            <div className="placeholder-content">
              <div className="placeholder-card">
                <h3>Goal Setting</h3>
                <p>Create new fitness goals</p>
              </div>
              <div className="placeholder-card">
                <h3>Goal Progress</h3>
                <p>Track your goal achievements</p>
              </div>
            </div>
          </div>
        )
      case 'profile':
        return (
          <div className="content-section">
            <h2>Profile Settings</h2>
            <p className="subtitle">Manage your account and preferences</p>
            <div className="placeholder-content">
              <div className="placeholder-card">
                <h3>Account Settings</h3>
                <p>Update your profile information</p>
              </div>
              <div className="placeholder-card">
                <h3>Preferences</h3>
                <p>Customize your app settings</p>
              </div>
            </div>
          </div>
        )
      default:
        return null
    }
  }

  // Helper function to get appropriate icon for each muscle group
  const getMuscleGroupIcon = (muscleGroup) => {
    const icons = {
      'abdominals': abdominalsIcon,
      'abductors': abductorsIcon,
      'adductors': adductorsIcon,
      'biceps': bicepsIcon,
      'calves': calvesIcon,
      'chest': chestIcon,
      'forearms': forearmsIcon,
      'glutes': glutesIcon,
      'hamstrings': hamstringsIcon,
      'lats': latsIcon,
      'lower back': lowerBackIcon,
      'middle back': middleBackIcon,
      'neck': neckIcon,
      'quadriceps': quadricepsIcon,
      'shoulders': shouldersIcon,
      'traps': trapsIcon,
      'triceps': tricepsIcon
    }
    
    const iconSrc = icons[muscleGroup]
    if (iconSrc) {
      return <img src={iconSrc} alt={`${muscleGroup} icon`} className="muscle-group-image" />
    }
    return <span>💪</span> // Fallback emoji
  }

  // Helper function to format muscle group names
  const formatMuscleGroupName = (muscleGroup) => {
    return muscleGroup
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  return (
    <div className={`dashboard-container ${sidebarHovered ? 'sidebar-expanded' : ''}`}>
      {/* Sidebar */}
      <aside 
        className={`sidebar ${sidebarHovered ? 'expanded' : 'collapsed'}`}
        onMouseEnter={handleSidebarMouseEnter}
        onMouseLeave={handleSidebarMouseLeave}
      >
        <div className="sidebar-header">
          <div className="brand">
            <img 
              src={appIcon} 
              alt="Fit.AI Icon" 
              className="brand-icon"
            />
            {sidebarHovered && (
              <div className="brand-text">
                <h2>Fit.AI</h2>
                <p>Fitness Management</p>
              </div>
            )}
          </div>
        </div>

        <nav className="sidebar-nav">
          <ul className="nav-list">
            {menuItems.map((item) => (
              <li key={item.id} className="nav-item">
                <button
                  className={`nav-button ${activeTab === item.id ? 'active' : ''}`}
                  onClick={() => setActiveTab(item.id)}
                  title={!sidebarHovered ? item.label : undefined}
                >
                  <span className="nav-icon">{item.icon}</span>
                  {sidebarHovered && (
                    <div className="nav-content">
                      <span className="nav-label">{item.label}</span>
                      <span className="nav-description">{item.description}</span>
                    </div>
                  )}
                </button>
              </li>
            ))}
          </ul>
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              <span>{user?.first_name?.charAt(0) || 'U'}</span>
            </div>
            {sidebarHovered && (
              <div className="user-details">
                <span className="user-name">{user?.first_name || 'User'}</span>
                <span className="user-email">{user?.email}</span>
              </div>
            )}
          </div>
          <button 
            onClick={handleLogout} 
            className="logout-button"
            title={!sidebarHovered ? "Logout" : undefined}
          >
            <img 
              src={logoutIcon} 
              alt="Logout" 
              className="logout-icon"
              onError={(e) => {
                console.error('Failed to load logout icon');
                e.target.style.display = 'none';
                // Add fallback text icon
                const fallback = document.createElement('span');
                fallback.textContent = '⏻';
                fallback.className = 'logout-icon-fallback';
                e.target.parentNode.insertBefore(fallback, e.target);
              }}
            />
            {sidebarHovered && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="content-header">
          <div className="header-content">
            <h1>{menuItems.find(item => item.id === activeTab)?.label}</h1>
            <div className="header-actions">
              <button className="notification-btn">
                <span>🔔</span>
              </button>
            </div>
          </div>
        </header>

        <div className="content-body">
          {renderContent()}
        </div>
      </main>
    </div>
  )
}

export default Dashboard 