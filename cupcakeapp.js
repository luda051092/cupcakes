$(async function () {
    const url = '/api/cupcakes'

    $('#list').empty()

    await getAllCupcakes();

    async function getAllCupcakes() {
        const resp = await axios.get(url);

        for (const cupcake of resp.data.cupcakes) {
            $('#list').append(` 
            <div class="col-lg-3 col-md-6 col-sm-10">
                <div class="card round shadow m-3 d-flex">
                    <div class="card-img-top">
                        <img src="${cupcake.image}" class="img-fluid w-auto" alt="${cupcake.flavor} cupcake">
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">
                        ${cupcake.flavor.charAt(0).toUpperCase() + cupcake.flavor.slice(1)}
                        </h5>
                        <p class="lead mt-3">Rating: ${cupcake.rating}</p>
                        <p class="lead">Size: ${cupcake.size}</p>
                    </div>
                </div>
            </div>
            `)
        }
    }

    $('form').on('submit', async function (e) {
        e.preventDefault();
        const flavor = $('#flavor').val();
        const size = $('#size').val();
        let rating = $('#rating').val();
        rating = parseFloat(rating);
        const image = $('#image').val();

        const data = {
            flavor, 
            size, 
            rating, 
            image
        };

        const resp = await axios.post(url, data);

        const newCupcake = resp.data.cupcake;

        $('#list').append(`
        <div class="col-lg-3 col-md-6 col-sm-10">
            <div class="card round shadow m-3 d-flex">
               <div class="card-img-top">
                   <img src="${cupcake.image}" class="img-fluid w-auto" alt="${cupcake.flavor} cupcake"> 
               </div>
               <div class="card-body">
                   <h5 class="card-title">
                   ${cupcake.flavor.charAt(0).toUpperCase() + cupcake.flavor.slice(1)}
                   </h5>
                   <p class="lead mt-3"> Rating: ${cupcake.rating}</p>
                   <p class="lead"> Size: ${cupcake.size}</p>
               </div> 
            </div>
        </div>  

        `);

        $('input').val('');

    });
})