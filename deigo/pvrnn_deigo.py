import toml

def main():
    config_file = 'example/example_config.toml'    
    config = toml.load(config_file)

    # assuming ${PVRNN_SAVE_DIR} is already set
    # new output dir ( This will resolve to: ${PVRNN_SAVE_DIR} / "results" / save_directory)
    config['training']['save_directory'] = 'train'

    # 4 layers in order: sm, second (bottom), third, forth (top)
    layers = config['network']['layers']    
    
    # changing w to last three layers
    new_w = [0.2, 0.3, 0.4]
    for i,l in enumerate(layers[1:]):
        l['w'] = new_w[i]

    new_config_file = 'example/auto_config.toml'
    with open(new_config_file, 'w') as fout:
        toml.dump(config, fout)
    # print(toml.dumps(config))

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--dir', type=str, help='Output directory')
    # args = parser.parse_args()

    main()