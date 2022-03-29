function search(id) {
    fetch(`http://localhost:5000/pokemon/?id=${id}`)
        .then(res => {
            if(res.ok) {
                console.log('SUCCESS')
                return res.json();
            }
            throw new Error('Not successful')
        })
        .then(data => console.log(data))
        .catch(error => console.error(error))
};