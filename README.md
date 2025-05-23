# 🥔 Potato Sentinel: Hybrid Intelligence for Healthier Crops  

## 🌟 Project Overview  
Potato Sentinel is an advanced web application designed to detect and diagnose potato leaf diseases using a hybrid intelligence approach. The system combines **deep learning (CNN)** with **traditional machine learning (Random Forest)** to provide accurate disease classification and detailed information to help farmers and agricultural professionals manage potato crop health effectively.  

---

## 🚀 Key Features  

### 🌱 Disease Detection  
- Identifies three conditions in potato leaves:  
  - **Early Blight** (*Alternaria solani*)  
  - **Late Blight** (*Phytophthora infestans*)  
  - **Healthy leaves*  

### 🤖 Hybrid Model Architecture  
- **CNN Ensemble**: Convolutional Neural Networks for feature extraction.  
- **Random Forest Classifier**: Final prediction layer.  
- **Standardized Feature Scaling**: Enhances model performance.  

### 🖥️ User-Friendly Interface  
- Simple **image upload functionality**.  
- Clear and concise **disease diagnosis results**.  
- Detailed descriptions of detected diseases.  
- **Responsive design** for desktop and mobile devices.  

### 📚 Educational Resources  
- Information about common potato diseases.  
- Prevention and treatment recommendations.  
- Links to scientific resources for further reading.  

---

## 🛠️ Technical Implementation  

### Machine Learning Pipeline  
1. **Data Processing**:  
   - Image resizing and normalization.  
   - Data augmentation (rotation, flipping, zooming, brightness/contrast adjustments).  
   - Dataset partitioning (training, validation, testing).  

2. **Model Architecture**:  
   - **CNN Ensemble**: Feature extraction.  
   - **Feature Concatenation**: Combines outputs from multiple CNN models.  
   - **Random Forest Classifier**: Final classification.  

3. **Training Process**:  
   - CNN training with augmented data.  
   - Feature extraction from trained CNN models.  
   - Random Forest training on extracted features.  

4. **Inference Pipeline**:  
   - Image preprocessing.  
   - Feature extraction using CNN ensemble.  
   - Feature standardization.  
   - Classification using Random Forest.  

### Web Application  
- **Backend**: Flask web framework.  
- **Frontend**: HTML, CSS, JavaScript.  
- **Image Processing**: TensorFlow and Keras.  
- **Model Deployment**: Pre-trained models loaded at runtime.  

---

## 📂 Project Structure  
Potato_Sentinel/
├── PlantVillage/ # Dataset directory
│ ├── Potato___Early_blight/ # Early blight images
│ ├── Potato___Late_blight/ # Late blight images
│ └── Potato___healthy/ # Healthy leaf images
├── static/ # Static assets
│ ├── images/ # UI images
│ ├── *.css # CSS stylesheets
│ └── *.js # JavaScript files
├── templates/ # HTML templates


---

## 🧰 Technologies Used  
- **Python**: Core programming language.  
- **TensorFlow/Keras**: Deep learning framework.  
- **scikit-learn**: Machine learning library.  
- **Flask**: Web framework.  
- **NumPy/Pandas**: Data manipulation.  
- **Matplotlib/Seaborn**: Data visualization.  
- **HTML/CSS/JavaScript**: Frontend development.  

---

