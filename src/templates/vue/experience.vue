<template>
<div class="card experience"
     :id="'exp' + expindex">
    <div class="card-body">

        <div class="d-flex justify-content-between">
            <div>
                <h5 class="card-title">
                    {{ expdict.title }}
                </h5>
                <h6 class="text-muted card-subtitle">
                    {{ expdict.dateStart.month }}, {{ expdict.dateStart.year }}
                    <span v-if="expdict.dateEnd">- {{ expdict.dateEnd.month }}, {{ expdict.dateEnd.year }}</span>
                </h6>
            </div>
            <div>
                <a :href="expdict.company.link">
                    <img class="card-img-side"
                         :src="static_url_cdn + expdict.company.logo"
                         :alt="expdict.company.name">
                </a>
            </div>
        </div>


        <div class="card-text mt-2">
            <span v-html="from_markdown_to_html(expdict.description)"></span>
        </div>

    </div>
    <div v-if="expdict.isCurrent"
         style="text-align: center;">
        <h6 style="align-self: center">
            <span class="badge badge-primary">Current</span>
        </h6>
    </div>
    <div class="card-footer">

        <a :class="'btn btn-sm btn-block ' + (isSelected ? 'btn-secondary' : 'btn-light') "
           @click.prevent="doSelect"
           href>
            <span v-if="!(isSelected)">
                Show Skills
            </span>
            <span v-else>
                Showing Skills
            </span>
        </a>

    </div>

</div>
</template>


<script>
export default {
    name: "exp",
    props: [
        "expdict",
        "expindex"
    ],
    data: function () {
        return {
            static_url_cdn: "https://static.claytonjroberts.com/"
        }
    },
    computed: {
        isSelected: function () {
            var self = this;
            return (self.expindex == self.$parent.selectedexperience);
        }
    },
    methods: {
        doSelect: function () {
            var self = this;
            if (self.isSelected) {
                self.$parent.selectedexperience = null;
            } else {
                self.$parent.selectedexperience = self.expindex;
            }
        },
        from_markdown_to_html: function (x) {
            return mdconverter.makeHtml(x);
        }

    },
}
</script>
