import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate, Link } from 'react-router-dom'
import appIcon from '../assets/app-icon.png'
import manWithDumbbell from '../assets/man-with-dumbbell.png'
import './Login.css'

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [keepLoggedIn, setKeepLoggedIn] = useState(false)
  const [imageLoaded, setImageLoaded] = useState(false)
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleImageLoad = () => {
    setImageLoaded(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    try {
      const success = await login(formData)
      if (success) {
        navigate('/dashboard')
      } else {
        setError('Invalid email or password')
      }
    } catch (err) {
      setError('Login failed. Please try again.')
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-left-panel">
          <div className="form-container">
            <div className="brand-section">
              <div className="logo">
                <img 
                  src={appIcon} 
                  alt="Fit.AI Icon" 
                  className="logo-image"
                  onLoad={handleImageLoad}
                />
                <div className="logo-text">
                  <h1>Fit.AI</h1>
                  <p>Fitness Management</p>
                </div>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="auth-form">
              <h2 className="form-title">Welcome Back</h2>
              <p className="form-subtitle">Sign in to your account to continue your fitness journey</p>
              
              {error && <div className="error-message">{error}</div>}
              
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <div className="input-wrapper">
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your email"
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <div className="input-wrapper">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? '👁️' : '👁️‍🗨️'}
                  </button>
                </div>
              </div>

              <div className="form-row">
                <label className="checkbox-container">
                  <input
                    type="checkbox"
                    checked={keepLoggedIn}
                    onChange={(e) => setKeepLoggedIn(e.target.checked)}
                  />
                  <span className="checkmark"></span>
                  Keep me logged in
                </label>
              </div>

              <button type="submit" className="submit-button">
                Sign In
              </button>
            </form>

            <div className="register-prompt">
              <span>Don't have an account? </span>
              <Link to="/signup" className="register-link">Sign up</Link>
            </div>

            <div className="footer-links">
              <a href="#" className="footer-link">Terms of Use</a>
              <span className="footer-separator">•</span>
              <a href="#" className="footer-link">Privacy Policy</a>
            </div>
          </div>
        </div>

        <div className="auth-right-panel">
          <div className="hero-image">
            <div className="image-container">
              <img
                src={manWithDumbbell}
                alt="Muscular bodybuilder performing bicep curl"
                className={`workout-image ${imageLoaded ? 'image-loaded' : ''}`}
                onLoad={handleImageLoad}
              />
              <div className="image-overlay">
                <div className="strength-indicator">
                  <div className="strength-bar"></div>
                  <div className="strength-text">STRENGTH</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login 