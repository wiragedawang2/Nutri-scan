async function uploadImage() {//accepting file gambar
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:8000/scan-barcode/', { // server backend sesuaikan yaa!!!
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to scan barcode');
        }

        const data = await response.json();
        displayResult(data);
    } catch (error) {
        console.error(error);
        alert(`Error scanning barcode: ${error.message}`);
    }
}

function displayResult(data) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    if (data.barcodes.length === 0) {
        resultDiv.innerHTML = '<p>No barcode detected.</p>';
        return;
    }

    data.barcodes.forEach(barcode => {
        const productInfo = barcode.product_info;

        function formatNutriments(nutriments) {
            let formattedString = "";
            for (const key in nutriments) {
                if (nutriments.hasOwnProperty(key)) {
                    formattedString += `${key}: ${nutriments[key]}<br>`;
                }
            }
            return formattedString;
        }

        let getTypes = document.getElementById('Types');
        let getDatas = document.getElementById('Datas');
        let getNames = document.getElementById('Names');
        let getBrands = document.getElementById('Brands');
        let getCategories = document.getElementById('Categories');
        let getNutries = document.getElementById('Nutries');
        let getImages = document.getElementById('product-image');
        let formulas = document.getElementById('Formula');
        let getEco = document.getElementById('Eco');

        getTypes.innerHTML = barcode.type;
        getDatas.innerHTML = barcode.data;
        getNames.innerHTML = productInfo.Nama_produk;
        getBrands.innerHTML = productInfo.Merk;
        getCategories.innerHTML = productInfo.kategory;
        getNutries.innerHTML = productInfo.Nilai_nutrisi;
        getImages.src = productInfo.Gambar;
        formulas.innerHTML = formatNutriments(productInfo.nutriments);
        getEco.innerHTML = productInfo.EcoLevel;
    });
}
