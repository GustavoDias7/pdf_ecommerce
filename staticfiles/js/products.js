const { createApp } = Vue;

createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      modal: {
        menu: false,
        logout: false,
      },
      products: [],
      productAPI: `${PRODUCT_API}?limit=3&offset=6`,
    };
  },
  methods: {
    openModal(name = "") {
      this.modal[name] = true;
    },
    closeModal(name = "") {
      this.modal[name] = false;
    },
    openLogout() {
      this.closeModal("menu");
      this.modal.logout = true;
    },
    closeLogout() {
      this.modal.logout = false;
    },
    showMore(id) {
      const $seeMore = document.getElementById(`see-more-${id}`);
      const $showMore = document.getElementById(`show-more-${id}`);

      if (!$seeMore.classList.contains("active")) {
        $seeMore.classList.add("active");
        $showMore.innerText = "mostrar menos";
      } else {
        $seeMore.classList.remove("active");
        $showMore.innerText = "mostrar mais";
      }
    },
    async getProducts() {
      if (this.productAPI !== null) {
        await fetch(this.productAPI)
          .then((r) => r.json())
          .then((r) => {
            this.products.push(...r.results);
            this.productAPI = r.next;
          })
          .catch((r) => console.log(r));
      } else {
        console.log("No more products!");
      }
    },
    cents_price(cents = 0) {
      return (cents / 100).toFixed(2).replace(".", ",");
    },
  },
  computed: {},
}).mount("#app");
