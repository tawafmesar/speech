<?php  
// login.php
include 'include/header.php';


?>

    <style>


    </style>
<!-- Header Start -->
<div class="jumbotron jumbotron-fluid position-relative overlay-bottom">
  <div class="container text-center">
  <div class="row g-3 w-100 align-items-center justify-content-between">
  <div class="col-lg-6" style="text-align: left;">
    <h3 class="mt-2 mb-2" style="color:#2a5c82;">
      Welcome to Speech Emotion Recognition. Our advanced system uses deep learning to analyze spoken language and detect emotional cues—providing insights for research, healthcare, and customer experience.
    </h3>
    <div class="mt-3">
      <a href="analyze.php" style="background-color:#2a5c82; color:azure;" class="btn btn-primary btn-outline-dark btn-lg px-5 py-3 ml-3">Analyze Audio</a>
    </div>
  </div>
  <div class="col-lg-5">
    <img src="./img/hero.png" alt="Speech Emotion Recognition" class="img-fluid rounded">
  </div>
</div>

  </div>
</div>
<!-- Header End -->

<div class="section about-us">
  <div class="container">
    <div class="row">
      <div class="col-lg-6 offset-lg-1">
        <div class="accordion" id="accordionExample">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingOne">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                How does our Speech Emotion Recognition work?
              </button>
            </h2>
            <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
              <div class="accordion-body">
                Our system leverages state-of-the-art deep learning models to extract audio features and predict the underlying emotion from speech samples.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingTwo">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                What emotions can be detected?
              </button>
            </h2>
            <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
              <div class="accordion-body">
                The system can detect a range of emotions including neutral, calm, happy, sad, angry, fear, disgust, and surprise.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingThree">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                How accurate is the analysis?
              </button>
            </h2>
            <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionExample">
              <div class="accordion-body">
                Our model is trained on a diverse dataset and achieves high accuracy, providing reliable emotion predictions across various speech samples.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingFour">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                What are the practical applications?
              </button>
            </h2>
            <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour" data-bs-parent="#accordionExample">
              <div class="accordion-body">
                From customer service and mental health assessments to interactive media, our technology offers valuable insights by analyzing emotional cues in speech.
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-5 align-self-center">
        <div class="section-heading">
          <h6>About Our System</h6>
          <h2>Advanced Speech Emotion Recognition</h2>
          <p>
            Our platform harnesses deep learning techniques to analyze and interpret speech emotions accurately. Enjoy real-time insights and a user-friendly interface designed for diverse applications.
          </p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Feature Start -->
<div class="container-fluid bg-image" style="margin: 90px 0;">
  <div class="container">
    <div class="row">
      <div class="col-lg-7 my-5 pt-5 pb-lg-5">
        <div class="section-title position-relative mb-4">
          <h6 class="d-inline-block position-relative text-secondary text-uppercase pb-2">Why Choose Our System?</h6>
          <h1 class="display-4">Leading the Future of Emotion Analysis</h1>
        </div>
        <p class="mb-4 pb-2">
          Our Speech Emotion Recognition system offers cutting-edge technology designed to deliver accurate, real-time emotion analysis. Experience seamless integration and powerful insights for your projects.
        </p>
        <div class="d-flex mb-3">
          <div class="btn-icon bg-primary mr-4">
            <i class="fa fa-2x fa-brain text-white"></i>
          </div>
          <div class="mt-n1">
            <h4>High Accuracy</h4>
            <p>
              Leveraging advanced deep learning algorithms, our system delivers precise emotion detection from diverse speech samples.
            </p>
          </div>
        </div>
        <div class="d-flex mb-3">
          <div class="btn-icon bg-secondary mr-4">
            <i class="fa fa-2x fa-bolt text-white"></i>
          </div>
          <div class="mt-n1">
            <h4>Real-time Analysis</h4>
            <p>
              Get immediate feedback on emotional cues with our optimized processing pipeline, ensuring timely insights for decision-making.
            </p>
          </div>
        </div>
        <div class="d-flex">
          <div class="btn-icon bg-warning mr-4">
            <i class="fa fa-2x fa-users text-white"></i>
          </div>
          <div class="mt-n1">
            <h4>Versatile Applications</h4>
            <p class="m-0">
              Adaptable across industries—from customer service to healthcare—our system empowers you to make data-driven improvements.
            </p>
          </div>
        </div>
      </div>
      <div class="col-lg-5" style="min-height: 500px;">
        <div class="position-relative h-100">
        <img class="position-absolute w-100 h-100" src="img/feature.png" style="object-fit: cover;" alt="Why Choose MONTALQ">

          <!-- <img class="position-absolute w-100 h-100" src="img/emotion_feature.png" style="object-fit: cover;" alt="Emotion Recognition Feature"> -->
        </div>
      </div>
    </div>
  </div>
</div>
<!-- Feature End -->

<?php include 'include/footer.php'; ?>