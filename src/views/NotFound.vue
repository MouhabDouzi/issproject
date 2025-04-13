<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you are looking for doesn't exist or has been moved.</p>
      <router-link to="/" class="btn btn-primary">Go Home</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
};
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  text-align: center;
}

.not-found-content {
  max-width: 500px;
  padding: 40px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 80px;
  margin: 0;
  color: #007bff;
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

p {
  margin-bottom: 30px;
  color: #666;
}

.btn {
  padding: 10px 20px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  display: inline-block;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
}
</style> 