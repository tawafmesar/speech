<?php 
include 'include/header.php';
?>

<div class="container my-5">
  <h1 class="text-center mb-4">Frequently Asked Questions</h1>
  <br><br>
  <div class="accordion" id="faqAccordion">
    <!-- FAQ Item 1 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="faqHeading1">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse1" aria-expanded="true" aria-controls="faqCollapse1">
          What is Speech Emotion Recognition?
        </button>
      </h2>
      <div id="faqCollapse1" class="accordion-collapse collapse show" aria-labelledby="faqHeading1" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          Speech Emotion Recognition is a technology that analyzes audio signals to determine the emotional state of the speaker using advanced deep learning algorithms.
        </div>
      </div>
    </div>
    <!-- FAQ Item 2 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="faqHeading2">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse2" aria-expanded="false" aria-controls="faqCollapse2">
          How does the system work?
        </button>
      </h2>
      <div id="faqCollapse2" class="accordion-collapse collapse" aria-labelledby="faqHeading2" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          The system extracts numerical features from audio recordings (e.g., MFCCs, zero-crossing rates) and uses a pre-trained deep learning model to classify the input into emotional categories.
        </div>
      </div>
    </div>
    <!-- FAQ Item 3 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="faqHeading3">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse3" aria-expanded="false" aria-controls="faqCollapse3">
          What emotions can be detected?
        </button>
      </h2>
      <div id="faqCollapse3" class="accordion-collapse collapse" aria-labelledby="faqHeading3" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          Our system is capable of detecting multiple emotions including neutral, calm, happy, sad, angry, fear, disgust, and surprise, making it versatile for various applications.
        </div>
      </div>
    </div>
    <!-- FAQ Item 4 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="faqHeading4">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse4" aria-expanded="false" aria-controls="faqCollapse4">
          How accurate is the emotion analysis?
        </button>
      </h2>
      <div id="faqCollapse4" class="accordion-collapse collapse" aria-labelledby="faqHeading4" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          Our deep learning model is trained on a diverse dataset and consistently achieves high accuracy. However, performance may vary depending on audio quality and background noise.
        </div>
      </div>
    </div>
    <!-- FAQ Item 5 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="faqHeading5">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse5" aria-expanded="false" aria-controls="faqCollapse5">
          What are the practical applications of this technology?
        </button>
      </h2>
      <div id="faqCollapse5" class="accordion-collapse collapse" aria-labelledby="faqHeading5" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          Applications range from enhancing customer service and user experience to aiding in mental health assessments and interactive media, providing valuable insights for various industries.
        </div>
      </div>
    </div>

    <!-- FAQ Item 6 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="faqHeading5">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse5" aria-expanded="false" aria-controls="faqCollapse5">
          How do I get started?
        </button>
      </h2>
      <div id="faqCollapse5" class="accordion-collapse collapse" aria-labelledby="faqHeading5" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          Getting started is easy! Simply register an account, explore our demo on the Analyze page, and feel free to reach out to our support team for any assistance or integration inquiries.
        </div>
      </div>
    </div>

        <!-- FAQ Item 7 -->
        <div class="accordion-item">
      <h2 class="accordion-header" id="faqHeading4">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse4" aria-expanded="false" aria-controls="faqCollapse4">
          How can I incorporate Speech Emotion Recognition in my workflow?
        </button>
      </h2>
      <div id="faqCollapse4" class="accordion-collapse collapse" aria-labelledby="faqHeading4" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          Integrating Speech Emotion Recognition into your workflow is simple. You can start by exploring our demo on the Analyze page to see the system in action. Once you’re comfortable with its capabilities, you can use the technology to monitor customer interactions, enhance training programs, or analyze feedback to improve service delivery.
        </div>
      </div>
    </div>
    <!-- FAQ Item 8 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="faqHeading8">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse8" aria-expanded="false" aria-controls="faqCollapse8">
          How do you ensure user data privacy and security?
        </button>
      </h2>
      <div id="faqCollapse8" class="accordion-collapse collapse" aria-labelledby="faqHeading8" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          User privacy and security are our top priorities. All audio data is processed securely, and we do not store your files without explicit permission. Our system follows industry-standard protocols to ensure that your data remains confidential and protected.
        </div>
      </div>
    </div>
<br><br>
  </div>
</div>

<?php 
include 'include/footer.php';
?>
