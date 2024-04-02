path "kv/data/myminio/*" {
   capabilities = [ "create", "read" ]
}
path "kv/metadata/myminio/*" {
   capabilities = [ "list", "delete" ]       
}
