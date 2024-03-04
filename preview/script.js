



// document.addEventListener("DOMContentLoaded", function() {
//     const oldValue = document.getElementById('oldvalue')
//     const newValue = document.getElementById("newvalue")
//     const measureValue = (value) => {
//         // Replace 'your-variable' with the actual variable value (0% to 100%)
//         let variable = parseInt(value); // Example value, replace with your actual variable value
    
//         // Calculate the rotation angle based on the percentage
//         const rotationAngle = (variable / 100) * 180;
    
//         // Apply the rotation to the image using CSS
//         const rotateImage = document.getElementById('rotateImage');
//         rotateImage.style.transform = 'rotate(' + rotationAngle + 'deg)';
//     }
    
    
//     measureValue(oldValue.innerHTML)
    
//     setTimeout(() => {
//         measureValue(newValue.innerHTML)
        
//     }, 3000);
// });