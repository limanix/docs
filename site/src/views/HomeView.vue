<script setup lang="ts">
import CatalogSection from '@/components/sections/CatalogSection.vue'
import ClosingSection from '@/components/sections/ClosingSection.vue'
import FaqSection from '@/components/sections/FaqSection.vue'
import FeaturesSection from '@/components/sections/FeaturesSection.vue'
import HeroSection from '@/components/sections/HeroSection.vue'
import HowItWorksSection from '@/components/sections/HowItWorksSection.vue'
import { siteContent } from '@/contents'

const { home, links } = siteContent
</script>

<template>
  <HeroSection :content="home.hero" :demo="home.demo" :links="links" />
  <FeaturesSection :content="home.features" />
  <HowItWorksSection :content="home.howItWorks" />
  <CatalogSection :content="home.catalog" />
  <FaqSection :content="home.faq" />
  <ClosingSection :content="home.closing" :links="links" />
</template>
