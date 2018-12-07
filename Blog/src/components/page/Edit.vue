<template>
  <Markdown :is-edit="true"/>
</template>

<script>
import Markdown from './Markdown'

export default {
  name: 'EditForm',
  components: { Markdown }
}
</script>