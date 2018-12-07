<template>
  <Markdown :is-edit="false"/>
</template>

<script>
import Markdown from './Markdown'

export default {
  name: 'CreateForm',
  components: { Markdown }
}
</script>