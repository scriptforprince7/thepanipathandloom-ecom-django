$(document).ready(function () {
  $(".add-to-cart-btn").off("click").on("click", function () {
    let this_val = $(this);
    let index = this_val.attr("data-index");
    let quantity = $(".product-quantity-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_id = $(".product-id-" + index).val();
    let product_price = $(".product-price-" + index).val();
    let product_price_wo_gst = $(".product-price-wo-gst-" + index).val();
    let gst_rate = $(".gst_rate-" + index).val();
    let gst_applied = $(".gst-applied-" + index).val();
    let product_sku = $(".product-sku-" + index).val();
    let product_image = $(".product-image-" + index).val();

    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("Price:", product_price);
    console.log("Price Without Gst:", product_price_wo_gst);
    console.log("gst_rate:", gst_rate);
    console.log("GST Applied:", gst_applied);
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
        gst_applied: gst_applied,
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
          updateCartItemsList(response.data);
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

function updateCartItemsList(cartData) {
  var cartItemsList = $(".product_list_widget");
  cartItemsList.empty();

  var subtotalAmount = 0;
  var baseUrl = "";

  // Update cart item count badge
  var cartItemCount = Object.keys(cartData).length;
  $("#cartItemCount").text(cartItemCount);
  $("#cartItemCountt").text(cartItemCount);
  $("#cartItemCounttt").text(cartItemCount);
  $("#cartItemCountttt").text(cartItemCount);

  if ($.isEmptyObject(cartData)) {
    var noProductsHtml = `
      <tr class="no-products-message">
        <td colspan="3" style="text-align: center;">
          <div style="text-align: center;">
            <img src="{% static 'images/no-product.png' %}" alt="Empty Cart Image" width="70%">
            <style>
              .explore:hover {
                background-color: #9fcfb5;
              }
            </style>
            <a href="/shop-category" style="text-align: center;">
              <button class="btn btn-success mt-3 d-block explore">Explore Categories</button>
            </a>
          </div>
        </td>
      </tr>`;
    cartItemsList.append(noProductsHtml);
  } else {
    $(".no-products-message").remove(); // Remove the no products message if present
    $(".fly-cart-footer").show();
// Remove the no products message if present

    $.each(cartData, function (productId, item) {
      var productUrl = generateProductUrl(baseUrl, item.title);
      var itemHtml = `
      <li class="woocommerce-mini-cart-item mini_cart_item">
                        <div class="product-thumbnail">
                                        <a href="">
                              <m-image class="minimog-lazy-image m-img-loaded" style="--lazy-image-width: 450px;--lazy-image-height: 100%;" intersecting="true"><img src="${item.image}" width="450" height="450" alt="${item.title}" loading="lazy" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail product-main-image-img"></m-image>							</a>
                                    </div>
              
                        <div class="product-info">
                          <h3 class="product-name post-title-2-rows">
                                            <a href="">
                                            ${item.title} x ${item.qty}						</a>
                                        </h3>
                          <dl class="variation">
                    <dt class="variation-Vendor">Sku:</dt>
                  <dd class="variation-Vendor"><p>${item.sku}</p>
              </dd>
                </dl>
              
                          <div class="product-price"><b><span class="woocommerce-Price-amount amount"><bdi><span class="woocommerce-Price-currencySymbol">₹</span> ${parseFloat(item.price).toFixed(2)}</bdi></span></b></div>
                          <div class="product-quantity-wrap">
                              <div class="quantity-button-wrapper">
                  <label class="screen-reader-text" aria-label="Malm High bed frame/4 storage boxes quantity">Quantity</label>
                  <div class="quantity">
                          <input
                           type="number"
                          class="input-text qty text update-product product-qty-${productId}"
                          data-product="${productId}"
                          data-sku="${item.sku}"
                          data-price="${item.price}"
                          value="${item.qty}"
                          size="4"
                          min="0"
                          max=""
                          step="1"
                          name="qty"
                          inputmode="numeric"
                          autocomplete="off" >
                      <button type="button" class="decrease update-product" data-product="${productId}" data-sku="${item.sku}" data-price="${item.price}">-</button>
                      <button type="button" class="increase update-product" data-product="${productId}" data-sku="${item.sku}" data-price="${item.price}">+</button>
                              </div>
                </div>
                            <button class="delete-product" data-product="${productId}">Remove</button>						
                          </div>
                        </div>
                      </li>`;
      cartItemsList.append(itemHtml);

      subtotalAmount += parseFloat(item.price) * item.qty;
    });

    $(".cart-subtotal").text(`₹ ${subtotalAmount.toFixed(2)}`);
  }
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
      customClass: {
        popup: 'swal2-top-zindex'  // Custom class to control z-index
      }
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

            // Refresh the page after a short delay
            setTimeout(function() {
              window.location.reload();
            }, 1000); // 500ms delay before refresh
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
      timer: 4000, // 2 seconds
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

    // Check if the clicked button is an increment or decrement button
    if ($(this).hasClass('increase')) {
      product_quantity = parseInt(product_quantity) + 1;
    } else if ($(this).hasClass('decrease')) {
      product_quantity = parseInt(product_quantity) - 1;
    }

    // Ensure quantity doesn't go below 1
    if (product_quantity < 1) {
      product_quantity = 1;
    }

    // Update the input field with the new quantity
    $(".product-qty-" + product_id).val(product_quantity);

    let product_sku = $(this).attr("data-sku");
    let product_price = $(this).attr("data-price");

    console.log("Product ID:", product_id);
    console.log("Product Qty:", product_quantity);
    console.log("Product SKU:", product_sku);
    console.log("Product Price:", product_price);

    $.ajax({
      url: "/update-cart",
      data: {
        id: product_id,
        qty: product_quantity,
        sku: product_sku,
        price: product_price,
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
          window.location.reload();
        }
      },
    });
  });
});



