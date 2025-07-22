import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate, Link } from 'react-router-dom'
import appIcon from '../assets/app-icon.png'
import manWithBarbell from '../assets/man-with-barbell.png'
import './Login.css'

function Signup() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm_password: '',
    date_of_birth: '',
    gender: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [imageLoaded, setImageLoaded] = useState(false)
  const [error, setError] = useState('')
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleImageLoad = () => {
    setImageLoaded(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match')
      return
    }
    
    // Remove confirm_password from the payload as it's not needed by the API
    const { confirm_password, ...signupData } = formData
    
    try {
      const success = await register(signupData)
      if (success) {
        navigate('/dashboard')
      } else {
        setError('Registration failed. Please try again.')
      }
    } catch (err) {
      setError('Registration failed. Please try again.')
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
              <h2 className="form-title">Create Account</h2>
              <p className="form-subtitle">Join Fit.AI to start your fitness journey</p>
              
              {error && <div className="error-message">{error}</div>}
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="first_name">First Name</label>
                  <div className="input-wrapper">
                    <input
                      type="text"
                      id="first_name"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleChange}
                      placeholder="Enter your first name"
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="last_name">Last Name</label>
                  <div className="input-wrapper">
                    <input
                      type="text"
                      id="last_name"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                      placeholder="Enter your last name"
                      required
                    />
                  </div>
                </div>
              </div>

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

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="date_of_birth">Date of Birth</label>
                  <div className="input-wrapper">
                    <input
                      type="date"
                      id="date_of_birth"
                      name="date_of_birth"
                      value={formData.date_of_birth}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="gender">Gender</label>
                  <div className="input-wrapper">
                    <select
                      id="gender"
                      name="gender"
                      value={formData.gender}
                      onChange={handleChange}
                      required
                    >
                      <option value="">Select gender</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
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

              <div className="form-group">
                <label htmlFor="confirm_password">Confirm Password</label>
                <div className="input-wrapper">
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    id="confirm_password"
                    name="confirm_password"
                    value={formData.confirm_password}
                    onChange={handleChange}
                    placeholder="Confirm your password"
                    required
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                  </button>
                </div>
              </div>

              <button type="submit" className="submit-button">
                Create Account
              </button>
            </form>

            <div className="register-prompt">
              <span>Already have an account? </span>
              <Link to="/login" className="register-link">Sign in</Link>
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
                src={manWithBarbell}
                alt="Powerful bodybuilder performing overhead lift with barbell"
                className={`workout-image ${imageLoaded ? 'image-loaded' : ''}`}
                onLoad={handleImageLoad}
              />
              <div className="image-overlay">
                <div className="strength-indicator">
                  <div className="strength-bar"></div>
                  <div className="strength-text">POWER</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Signup 