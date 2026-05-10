<template>
  <div class="turo-logo" :class="{ light }">
    <img
      src="/images/TURO_LOGO_WITH_MEANING.png"
      alt="TURO"
      class="logo-img"
    />
  </div>
</template>

<script setup>
defineProps({
  light: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.turo-logo {
  display: inline-flex;
  align-items: center;
}

.logo-img {
  width: 100%;
  max-width: 100%;
  height: 100px;
  object-fit: contain;
}

.turo-logo.light .logo-img {
  filter: brightness(0) invert(1);
}
</style>
