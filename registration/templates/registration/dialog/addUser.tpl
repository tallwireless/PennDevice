<script>

$( "#addUser button" ).on("click", handleAddUserForm);

</script>
<div class='addUserForm'>

<form id='addUser'>
<div class='instructions'>
Please enter the PennKey of the user you would like to add to this group.
</div>
<div class='fields'>
    <div class="row" id='row-mac'>
        <div class="label">PennKey</div>
        <div class="field"><input name='pennkey' id='pennkey' maxlength=20 size=20></div>
        <div id="user-err" class="hidden"></div>
</div>
<div class="buttons">
<button id='cancel'>Cancel</button><div
class='float-right'><button id='saveadd'> Save &amp; Add</button><button
id='save'>Save</button></div>
</div>
</div>
</div>
