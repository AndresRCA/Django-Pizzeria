function getCookie(name) {
  //https://docs.djangoproject.com/en/3.0/ref/csrf/
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

class Order {
  constructor(first_name, last_name, pizzas) {
    this.first_name = first_name
    this.last_name = last_name
    this.pizzas = pizzas // [Pizza]
  }
}

class Pizza {
	constructor(size, toppings) {
		this.size = size // size object
		this.toppings = toppings // [Topping]
	}

  getTotal() {
    let total = 0.00
    total += this.size.price
    this.toppings.forEach(topping => {
      total += topping.price
    })
    return total
  }

  getToppingNames() {
    let topping_names = this.toppings.map(topping => topping.name)
    return topping_names
  }
}

var app = new Vue({
	delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    first_name: '',
    last_name: '',
  	sizes: [], // sizes received from backend: {id, name, price}
  	selected_size: {}, // size object
  	toppings: [], // toppings received from backend: {id, name, price}
  	selected_toppings: [],
  	pizzas: [], // array of Pizza objects
    error: {
      message: '',
      isOn: false
    }
  },
  computed: {
  	size_price() {
  		return this.selected_size.price
  	},
    order_total() {
      let total = 0.00
      this.pizzas.forEach(pizza => {
        total += pizza.getTotal()
      })
      return total
    }
  },
  methods: {
    addTopping(id) {
      let topping = this.toppings.find(topping => topping.id == id)
      this.selected_toppings.push(topping)
    },
  	removeToppingFromSelected(index) {
  		this.selected_toppings.splice(index, 1)
  	},
  	addPizza() {
      let toppings_copy = Array.from(this.selected_toppings) // get shallow copy
      let pizza = new Pizza(this.selected_size, toppings_copy)
  		this.pizzas.push(pizza)
  	},
    removePizza(index) {
      this.pizzas.splice(index, 1)
    },
    placeOrder: async function() {
      let pizzas_copy = Array.from(this.pizzas)
      const order = new Order(this.first_name, this.last_name, pizzas_copy)

      try {
        let response = await fetch('/ordenar/', {
          method: 'POST',
          mode: 'same-origin',
          body: JSON.stringify(order),
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': getCookie('csrftoken')
          }
        })

        if(response.status != 200) { // throw error to handle it inside catch(){}
          let error_message = await response.text()
          throw new Error(error_message)
        }
        
        let res_message = await response.text()
        console.log(res_message) // the response was successful
        window.location.href = '/ordenar/confirmar' // redirect to confirmation view
      } catch(e) {
        console.log(e)
		this.error.message = e
		this.error.isOn = true
      }
    },
    deleteErrorMessage() {
      this.error.isOn = false
    }
  },
  filters: {
  	capitalize(value) {
  		if (!value) return ''
  		value = value.toString()
  		return value.charAt(0).toUpperCase() + value.slice(1)
  	},
  	currency(value) {
  		if (!value) return ''
  		return "$" + Number.parseFloat(value).toFixed(2)
  	}
  },
  created() {
    this.sizes = sizes
    this.toppings = toppings
    this.selected_size = sizes[0]
  }
})