document.addEventListener("DOMContentLoaded", function() {
    // URL de tu API en Vercel (actualiza esta URL con la que tu backend tenga)
    const apiUrl = "https://sms-api-coral.vercel.app/api/sms"; 

    // Función para obtener los SMS desde la API
    function fetchSMS() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                const smsList = data.messages; // Ajusta esto según la respuesta de tu API
                const smsContainer = document.getElementById("sms-list");
                smsContainer.innerHTML = ''; // Limpiar contenido actual

                smsList.forEach(sms => {
                    const smsElement = document.createElement("div");
                    smsElement.classList.add("sms-message");
                    smsElement.innerHTML = `
                        <p class="sender">From: ${sms.sender}</p>
                        <p><strong>Message:</strong> ${sms.message}</p>
                        <p><strong>Time:</strong> ${sms.time}</p>
                        <p><strong>PIN:</strong> ${sms.pin || "No PIN found"}</p>
                    `;
                    smsContainer.appendChild(smsElement);
                });
            })
            .catch(error => {
                console.error("Error fetching SMS data:", error);
            });
    }

    // Llamar a la función al cargar la página
    fetchSMS();
});
