<template>
  <div class="about-container">
    <h1>About TravelPlanner</h1>
    
    <div class="about-section">
      <h2>Our Mission</h2>
      <p>
        TravelPlanner is designed to make travel planning easier, more personalized, and more enjoyable.
        We believe that everyone deserves to experience the world, and our mission is to help you create
        the perfect travel itinerary tailored to your preferences, budget, and interests.
      </p>
    </div>
    
    <div class="about-section">
      <h2>How It Works</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>Personalized Recommendations</h3>
          <p>
            Our AI-powered system analyzes your preferences to suggest destinations that match your
            interests, budget, and travel style.
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">📅</div>
          <h3>Detailed Itineraries</h3>
          <p>
            Get day-by-day itineraries with activities, transportation options, and local tips to make
            the most of your trip.
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">💰</div>
          <h3>Budget Planning</h3>
          <p>
            Understand the costs involved in your trip, from accommodation to activities, so you can
            plan your budget accordingly.
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">👥</div>
          <h3>Community Features</h3>
          <p>
            Share your travel plans, discover plans created by others, and get inspired for your next adventure.
          </p>
        </div>
      </div>
    </div>
    
    <div class="about-section">
      <h2>Our Technology</h2>
      <p>
        TravelPlanner leverages cutting-edge AI technology to provide intelligent travel recommendations.
        Our system considers factors such as:
      </p>
      <ul class="tech-list">
        <li>Your budget preferences</li>
        <li>Preferred climate and weather conditions</li>
        <li>Travel purpose (leisure, adventure, cultural, business)</li>
        <li>Duration of your trip</li>
        <li>Number of travelers</li>
        <li>Special requirements or interests</li>
      </ul>
      <p>
        By analyzing these factors, we create personalized travel plans that help you discover new
        destinations and make the most of your travel experience.
      </p>
    </div>
    
    <div class="about-section">
      <h2>Contact Us</h2>
      <p>
        Have questions or feedback? We'd love to hear from you!
      </p>
      <div class="contact-info">
        <p><strong>Email:</strong> support@travelplanner.com</p>
        <p><strong>Phone:</strong> +1 (555) 123-4567</p>
        <p><strong>Address:</strong> 123 Travel Street, Adventure City, AC 12345</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
};
</script>

<style scoped>
.about-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
}

.about-section {
  margin-bottom: 50px;
}

h2 {
  margin-bottom: 20px;
  color: #007bff;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

p {
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.feature-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.feature-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

.tech-list {
  padding-left: 20px;
  margin-bottom: 20px;
}

.tech-list li {
  margin-bottom: 10px;
  color: #555;
}

.contact-info {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.contact-info p {
  margin-bottom: 10px;
}
</style> 