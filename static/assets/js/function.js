$(document).ready(function () {
  $(".add-to-cart-btn").on("click", function () {
    let this_val = $(this);
    let index = this_val.data("index");
    let quantity = $(".product-quantity-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_id = $(".product-id-" + index).val();
    let product_price = $(".product-price-" + index).val();
    let product_price_wo_gst = $(".product-price-wo-gst-" + index).val();
    let gst_rate = $(".gst_rate-" + index).val();
    let product_sku = $(".product-sku-" + index).val();
    let product_image = $(".product-image-" + index).val();

    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("Price:", product_price);
    console.log("Price Without Gst:", product_price_wo_gst);
    console.log("gst_rate:", gst_rate);
    console.log("ID:", product_id);
    console.log("Image:", product_image);
    console.log("Sku:", product_sku);
    console.log("Index:", index);
    console.log("Current Element:", this_val);

    $.ajax({
      url: "/add-to-cart",
      data: {
        id: product_id,
        image: product_image,
        qty: quantity,
        title: product_title,
        price: product_price,
        price_wo_gst: product_price_wo_gst,
        gst_rate: gst_rate,
        sku: product_sku,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Adding Product to the cart...");
      },
      success: function (response) {
        if (response.already_in_cart) {
          // Show alert that product is already in the cart
          Swal.fire({
            position: "top-end",
            icon: "info",
            title: "Product is already in your cart",
            showConfirmButton: false,
            timer: 1500,
          });
        } else {
          // Show success alert and update cart
          this_val.html("✓");
          console.log("Added Product to cart!");
          $(".cart-items-count").text(response.totalcartitems);

          Swal.fire({
            position: "top-end",
            icon: "success",
            title: "Product has been added to your cart",
            showConfirmButton: false,
            timer: 1500,
          });
        }
      },
    });
  });
});




function cleanTitle(title) {
  // Use a regex to remove the variant part (e.g., "- (50Pcs)")
  return title.replace(/\s*-\s*\(.*?\)$/, "");
}

function generateProductUrl(baseUrl, title) {
  var cleanedTitle = cleanTitle(title);
  // Encode the cleaned title to be URL-safe
  var encodedTitle = encodeURIComponent(cleanedTitle);
  return `${baseUrl}${encodedTitle}/`;
}


$(document).ready(function () {
  // Event delegation for delete buttons
  $(document).on("click", ".delete-product", function () {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    console.log("Product ID:", product_id);

    // Display SweetAlert confirmation dialog
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        // User confirmed the deletion, proceed with AJAX request
        $.ajax({
          url: "/delete-from-cart",
          data: {
            id: product_id,
            refresh_page: true, // Add a parameter to indicate page refresh
          },
          dataType: "json",
          beforeSend: function () {
            this_val.hide();
          },
          success: function (response) {
            this_val.show();
            $(".cart-items-count").text(response.totalcartitems);
            $("#cart-list").html(response.data);

            // Set a flag in local storage before refreshing the page
            localStorage.setItem("productDeleted", "true");

            // Refresh the page
            window.location.reload();
          },
        });
      }
    });
  });

  // Check if the productDeleted flag is set in local storage
  if (localStorage.getItem("productDeleted") === "true") {
    // Show the alert that the product is deleted
    Swal.fire({
      title: "Deleted!",
      text: "Product has been deleted.",
      icon: "success",
      timer: 2000, // 1 second
      confirmButtonText: "OK",
    });

    // Remove the flag from local storage
    localStorage.removeItem("productDeleted");
  }
});


$(document).ready(function () {
  $(".update-product").on("click", function () {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);
    let product_quantity = $(".product-qty-" + product_id).val();

    console.log("Product ID:", product_id);
    console.log("Product Qty:", product_quantity);

    $.ajax({
      url: "/update-cart",
      data: {
        id: product_id,
        qty: product_quantity,
        refresh_page: true,
      },
      dataType: "json",
      beforeSend: function () {
        this_val.hide();
      },
      success: function (response) {
        this_val.show();
        $(".cart-items-count").text(response.totalcartitems);
        $("#cart-list").html(response.data);

        if (response.refresh_page) {
          // Refresh the page
          window.location.reload();
        }
      },
    });
  });
});


