$(document).ready(function(){


    // top sale owl carousel
    $("#top-sale .owl-carousel").owlCarousel({
        loop:false,
        nav:true,
        dots:false,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:4
            },
            1000:{
                items:5
            }
        }

    });
    // favourites owl carousel
    $("#favourites .owl-carousel").owlCarousel({
        loop:false,
        nav:true,
        dots:false,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:4
            },
            1000:{
                items:5
            }
        }

    });

    // isotope filter
    var $grid = $(".grid").isotope({
        itemSelector : '.grid-item',
        layoutMode : 'fitRows'
    });


    // filter items on button click
    $(".button-group").on("click", "button", function(){
        var filterValue = $(this).attr('data-filter');
        $grid.isotope({ filter: filterValue});
    })


});

document.getElementById("placeOrderFinal").addEventListener("click", function() {
    document.getElementById("checkoutForm").submit();
  });

  // Get all list items in the navigation bar
var navItems = document.querySelectorAll('.navbar-nav .nav-item');

// Add an event listener to each list item
navItems.forEach(function(item) {
  item.addEventListener('click', function() {
    // Remove the active class from all list items
    navItems.forEach(function(item) {
      item.classList.remove('activeMenuItem');
    });
    
    // Add the active class to the selected list item
    item.classList.add('activeMenuItem');
  });
});

