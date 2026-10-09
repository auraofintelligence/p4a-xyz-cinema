/* Filtering is progressive enhancement: all policy content is present in HTML. */
(function(){'use strict';
 const controls=document.querySelector('[data-policy-filters]');if(!controls)return;
 const query=document.querySelector('[data-policy-search]'),category=document.querySelector('[data-policy-category-filter]'),reset=document.querySelector('[data-policy-reset]'),count=document.querySelector('[data-policy-count]'),empty=document.querySelector('[data-policy-empty]');
 const cards=[...document.querySelectorAll('[data-policy-entry]')],groups=[...document.querySelectorAll('[data-policy-group]')];
 const texts=new Map(cards.map(card=>[card,card.textContent.toLocaleLowerCase('en-AU')]));
 function filter(){const term=query.value.trim().toLocaleLowerCase('en-AU');let visible=0;cards.forEach(card=>{card.hidden=!!((category.value&&card.dataset.policyCategory!==category.value)||(term&&!texts.get(card).includes(term)));if(!card.hidden)visible++;});groups.forEach(group=>{group.hidden=![...group.querySelectorAll('[data-policy-entry]')].some(card=>!card.hidden);});count.textContent=visible===cards.length?'All '+cards.length+' policy ideas':visible+' of '+cards.length+' policy ideas';empty.hidden=visible!==0;}
 controls.hidden=false;query.addEventListener('input',filter);category.addEventListener('change',filter);reset.addEventListener('click',()=>{query.value='';category.value='';filter();query.focus();});filter();
})();
